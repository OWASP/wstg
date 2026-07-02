const http = require('http');
const fs = require('fs');
const fsp = require('fs/promises');
const path = require('path');

const ROOT_DIR = __dirname;
loadDotEnv(path.join(ROOT_DIR, '.env'));

const APP_DIR = path.join(ROOT_DIR, 'wstg_checklist_app');
const PORT = Number(process.env.PORT || 3000);
const HOST = process.env.HOST || '127.0.0.1';
const JSON_BODY_LIMIT = 10 * 1024 * 1024;
const DEFAULT_MISSING_TEMPLATES_FILE = 'sysreptor_missing_templates.md';

class AppError extends Error {
    constructor(status, message, details = null) {
        super(message);
        this.status = status;
        this.details = details;
        this.sysreptorStatus = null;
    }
}

class SysReptorClient {
    constructor({ url, token }) {
        this.baseUrl = normalizeBaseUrl(url);
        this.token = token;
    }

    async requestUrl(method, url, body = null) {
        const response = await fetch(url, {
            method,
            headers: {
                'User-Agent': 'owasp-wstg-checklist-app',
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            },
            body: body === null ? undefined : JSON.stringify(body),
            redirect: 'manual'
        });

        const text = await response.text();
        const data = parseJsonOrText(text);

        if (response.status >= 300 && response.status < 400) {
            throw new AppError(
                502,
                `SysReptor redirected the API request to ${response.headers.get('location') || 'another URL'}. Check SYSREPTOR_URL.`,
                data
            );
        }

        if (!response.ok) {
            const error = new AppError(
                502,
                sysreptorErrorMessage(response.status, response.statusText, data),
                data
            );
            error.sysreptorStatus = response.status;
            throw error;
        }

        return data;
    }

    async request(method, apiPath, body = null) {
        return this.requestUrl(method, `${this.baseUrl}${apiPath}`, body);
    }

    async getPaginated(apiPath, params = {}) {
        const url = new URL(`${this.baseUrl}${apiPath}`);
        Object.entries(params).forEach(([key, value]) => {
            if (value !== undefined && value !== null && value !== '') {
                url.searchParams.set(key, value);
            }
        });

        const results = [];
        let nextUrl = url.toString();

        while (nextUrl) {
            const data = await this.requestUrl('GET', nextUrl);
            if (Array.isArray(data)) {
                results.push(...data);
                break;
            }

            results.push(...(data.results || []));
            nextUrl = data.next || '';
        }

        return results;
    }

    async createProject(name, projectDesign, tags) {
        return this.request('POST', '/api/v1/pentestprojects/', {
            name,
            project_type: projectDesign,
            tags
        });
    }

    async getProject(projectId) {
        return this.request('GET', `/api/v1/pentestprojects/${encodeURIComponent(projectId)}/`);
    }

    async getFindings(projectId) {
        const findings = await this.request('GET', `/api/v1/pentestprojects/${encodeURIComponent(projectId)}/findings/`);
        return Array.isArray(findings) ? findings : [];
    }

    async createFinding(projectId, payload) {
        return this.request('POST', `/api/v1/pentestprojects/${encodeURIComponent(projectId)}/findings/`, payload);
    }

    async createFindingFromTemplate(projectId, templateId, language) {
        const payload = { template: templateId };
        if (language) {
            payload.template_language = language;
        }
        return this.request('POST', `/api/v1/pentestprojects/${encodeURIComponent(projectId)}/findings/fromtemplate/`, payload);
    }

    async getFindingTemplatesByTag(tag) {
        const templates = await this.getPaginated('/api/v1/findingtemplates/', { search: tag });
        return templates.filter(template => Array.isArray(template.tags) && template.tags.includes(tag));
    }
}

function loadDotEnv(filePath) {
    if (!fs.existsSync(filePath)) return;

    const content = fs.readFileSync(filePath, 'utf8');
    for (const rawLine of content.split(/\r?\n/)) {
        const line = rawLine.trim();
        if (!line || line.startsWith('#')) continue;

        const separatorIndex = line.indexOf('=');
        if (separatorIndex === -1) continue;

        const key = line.slice(0, separatorIndex).trim();
        let value = line.slice(separatorIndex + 1).trim();
        if (!key || Object.prototype.hasOwnProperty.call(process.env, key)) continue;

        if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
            value = value.slice(1, -1);
        }
        process.env[key] = value;
    }
}

function getConfig() {
    const url = (process.env.SYSREPTOR_URL || process.env.REPTOR_SERVER || '').trim();
    const token = (process.env.SYSREPTOR_TOKEN || process.env.REPTOR_TOKEN || '').trim();
    const projectId = (process.env.SYSREPTOR_PROJECT_ID || process.env.REPTOR_PROJECT_ID || '').trim();
    const projectDesign = (process.env.SYSREPTOR_PROJECT_DESIGN || process.env.REPTOR_PROJECT_DESIGN || '').trim();

    const missing = [];
    if (!url) missing.push('SYSREPTOR_URL');
    if (!token) missing.push('SYSREPTOR_TOKEN');
    if (!projectId && !projectDesign) missing.push('SYSREPTOR_PROJECT_DESIGN');

    if (missing.length > 0) {
        throw new AppError(
            500,
            `Missing SysReptor configuration: ${missing.join(', ')}. Update .env and restart the server.`
        );
    }

    return {
        url,
        token,
        projectId,
        projectDesign,
        language: (process.env.SYSREPTOR_LANGUAGE || 'de-DE').trim(),
        placeholderLanguage: normalizePlaceholderLanguage(process.env.SYSREPTOR_PLACEHOLDER_LANGUAGE),
        findingStatus: (process.env.SYSREPTOR_FINDING_STATUS || 'in-progress').trim(),
        missingTemplateSeverity: normalizeSeverity(process.env.SYSREPTOR_MISSING_TEMPLATE_SEVERITY),
        missingTemplateCvss: (process.env.SYSREPTOR_MISSING_TEMPLATE_CVSS || 'n/a').trim(),
        summaryField: (process.env.SYSREPTOR_SUMMARY_FIELD || 'summary').trim(),
        descriptionField: (process.env.SYSREPTOR_DESCRIPTION_FIELD || 'description').trim(),
        recommendationField: (process.env.SYSREPTOR_RECOMMENDATION_FIELD || 'recommendation').trim(),
        stepsField: (process.env.SYSREPTOR_STEPS_FIELD || 'steps').trim(),
        allowDuplicates: parseBoolean(process.env.SYSREPTOR_ALLOW_DUPLICATES),
        fallbackOnTemplateError: parseBoolean(process.env.SYSREPTOR_FALLBACK_ON_TEMPLATE_ERROR, true),
        templateTag: (process.env.SYSREPTOR_TEMPLATE_TAG || 'web').trim(),
        missingTemplatesFile: (process.env.SYSREPTOR_MISSING_TEMPLATES_FILE || DEFAULT_MISSING_TEMPLATES_FILE).trim(),
        tags: sortedUnique(['owasp-wstg', 'checklist-generated', ...parseCsv(process.env.SYSREPTOR_TAGS)])
    };
}

function normalizeBaseUrl(url) {
    return url.replace(/\/+$/, '');
}

function normalizePlaceholderLanguage(language) {
    return language === 'en-US' ? 'en-US' : 'de-DE';
}

function normalizeSeverity(severity) {
    const value = (severity || 'info').trim().toLowerCase();
    return ['info', 'low', 'medium', 'high', 'critical'].includes(value) ? value : 'info';
}

function parseBoolean(value, defaultValue = false) {
    const normalized = String(value || '').trim().toLowerCase();
    if (!normalized) return defaultValue;
    if (['1', 'true', 'yes', 'on'].includes(normalized)) return true;
    if (['0', 'false', 'no', 'off'].includes(normalized)) return false;
    return defaultValue;
}

function parseCsv(value) {
    return String(value || '')
        .split(',')
        .map(item => item.trim())
        .filter(Boolean);
}

function sortedUnique(values) {
    return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b));
}

function parseJsonOrText(text) {
    if (!text) return null;
    try {
        return JSON.parse(text);
    } catch {
        return text;
    }
}

function sysreptorErrorMessage(status, statusText, data) {
    if (data && typeof data === 'object') {
        if (data.detail) return `SysReptor API error ${status}: ${data.detail}`;
        if (data.error) return `SysReptor API error ${status}: ${data.error}`;
        if (data.message) return `SysReptor API error ${status}: ${data.message}`;
    }
    if (typeof data === 'string' && data.trim()) {
        return `SysReptor API error ${status}: ${data.slice(0, 300)}`;
    }
    return `SysReptor API error ${status}: ${statusText}`;
}

function normalizeTitle(title) {
    return String(title || '')
        .normalize('NFKC')
        .replace(/\s+/g, ' ')
        .trim()
        .toLocaleLowerCase();
}

function templateTitles(template) {
    const titles = [];
    if (template.title) titles.push(String(template.title));
    for (const translation of template.translations || []) {
        const title = translation && translation.data && translation.data.title;
        if (title) titles.push(String(title));
    }
    return sortedUnique(titles);
}

function buildTemplateTitleIndex(templates) {
    const index = new Map();
    const duplicates = [];

    for (const template of templates) {
        for (const title of templateTitles(template)) {
            const normalized = normalizeTitle(title);
            if (!normalized) continue;

            if (index.has(normalized) && index.get(normalized).id !== template.id) {
                duplicates.push({
                    title,
                    firstTemplateId: index.get(normalized).id,
                    duplicateTemplateId: template.id
                });
                continue;
            }

            index.set(normalized, {
                id: String(template.id),
                title,
                raw: template
            });
        }
    }

    return { index, duplicates };
}

function findTemplateForFinding(finding, templateIndex) {
    for (const title of finding.titleCandidates) {
        const match = templateIndex.get(normalizeTitle(title));
        if (match) {
            return match;
        }
    }
    return null;
}

function resolveTemplatesFromTitles(findings, templates) {
    const { index, duplicates } = buildTemplateTitleIndex(templates);
    const missingTemplates = [];

    const resolvedFindings = findings.map(finding => {
        const matchedTemplate = findTemplateForFinding(finding, index);
        if (!matchedTemplate) {
            missingTemplates.push(finding);
            return {
                ...finding,
                templateId: null,
                templateTitle: ''
            };
        }

        return {
            ...finding,
            templateId: matchedTemplate.id,
            templateTitle: matchedTemplate.title
        };
    });

    return { findings: resolvedFindings, missingTemplates, duplicateTemplateTitles: duplicates };
}

function collectFindings(checklist) {
    if (!checklist || typeof checklist !== 'object' || Array.isArray(checklist)) {
        throw new AppError(400, 'Checklist must be an object keyed by WSTG ID.');
    }

    const findings = [];
    for (const [wstgId, module] of Object.entries(checklist)) {
        if (!module || typeof module !== 'object' || Array.isArray(module)) continue;

        const rawFindings = module.sysreptor_findings || [];
        if (!Array.isArray(rawFindings)) {
            throw new AppError(400, `${wstgId}: sysreptor_findings must be a list.`);
        }

        rawFindings.forEach((rawFinding, index) => {
            if (!rawFinding || typeof rawFinding !== 'object' || Array.isArray(rawFinding)) {
                throw new AppError(400, `${wstgId}: sysreptor_findings[${index + 1}] must be an object.`);
            }

            const checklistFindingId = String(rawFinding.id || `${wstgId}-${index + 1}`);
            const titleCandidates = sortedUnique([
                rawFinding.name,
                rawFinding.title,
                rawFinding.title_en,
                rawFinding.title_de,
                rawFinding.title_custom
            ].map(value => String(value || '').trim()).filter(Boolean));

            findings.push({
                wstgId: String(wstgId),
                moduleStatus: String(module.status || ''),
                moduleTitle: String(module.title || wstgId),
                checklistFindingId,
                name: titleCandidates[0] || checklistFindingId,
                titleCandidates,
                templateId: null,
                templateTitle: ''
            });
        });
    }

    return findings;
}

function placeholderTextDe(finding) {
    return {
        summary: `Aus der Checkliste wurde der Befund **${finding.checklistFindingId}** im Modul **${finding.wstgId}** ausgewaehlt. Fuer diesen Befund existiert noch keine SysReptor-Vorlage.`,
        description: `TODO: Technische Beschreibung und Nachweise fuer **${finding.name}** ergaenzen.\n\nChecklisten-Modul: ${finding.moduleTitle}`,
        recommendation: 'TODO: Konkrete Massnahmen zur Behebung des Befunds ergaenzen.',
        steps: `TODO: Reproduktionsschritte, betroffene URLs/Parameter und Screenshots fuer **${finding.checklistFindingId}** ergaenzen.`
    };
}

function placeholderTextEn(finding) {
    return {
        summary: `Checklist finding **${finding.checklistFindingId}** from module **${finding.wstgId}** was selected. No reusable SysReptor template exists for this finding yet.`,
        description: `TODO: Add the technical description and evidence for **${finding.name}**.\n\nChecklist module: ${finding.moduleTitle}`,
        recommendation: 'TODO: Add concrete remediation guidance for this finding.',
        steps: `TODO: Add reproduction steps, affected URLs/parameters, and screenshots for **${finding.checklistFindingId}**.`
    };
}

function buildPlaceholderPayload(finding, config, order) {
    const text = config.placeholderLanguage === 'en-US' ? placeholderTextEn(finding) : placeholderTextDe(finding);

    return {
        status: config.findingStatus,
        order,
        data: {
            title: finding.name,
            cvss: config.missingTemplateCvss,
            severity: config.missingTemplateSeverity,
            [config.summaryField]: text.summary,
            [config.descriptionField]: text.description,
            [config.recommendationField]: text.recommendation,
            [config.stepsField]: text.steps,
            references: [],
            affected_components: []
        }
    };
}

function resultFor(status, action, projectId, projectName, finding, findingId = '') {
    return {
        status,
        action,
        projectId,
        projectName,
        wstgId: finding.wstgId,
        checklistFindingId: finding.checklistFindingId,
        templateId: finding.templateId || '',
        templateTitle: finding.templateTitle || '',
        findingId,
        title: finding.name
    };
}

function resolveWorkspaceOutputPath(fileName) {
    const safeFileName = fileName || DEFAULT_MISSING_TEMPLATES_FILE;
    const resolvedPath = path.resolve(ROOT_DIR, safeFileName);

    if (!resolvedPath.startsWith(ROOT_DIR + path.sep) && resolvedPath !== ROOT_DIR) {
        throw new AppError(400, 'SYSREPTOR_MISSING_TEMPLATES_FILE must point inside the repository.');
    }

    return resolvedPath;
}

function markdownTableCell(value) {
    return String(value || '')
        .replace(/\r?\n/g, '<br>')
        .replace(/\|/g, '\\|');
}

async function writeMissingTemplatesFile(missingTemplates, config, projectName, duplicateTemplateTitles = []) {
    const outputPath = resolveWorkspaceOutputPath(config.missingTemplatesFile);
    await fsp.mkdir(path.dirname(outputPath), { recursive: true });

    const lines = [
        '# Missing SysReptor Templates',
        '',
        `Generated: ${new Date().toISOString()}`,
        `Report title: ${projectName}`,
        `Template tag searched: ${config.templateTag}`,
        '',
    ];

    if (missingTemplates.length === 0) {
        lines.push('No missing templates for the last report generation run.', '');
    } else {
        lines.push('| Checklist ID | Module | Expected template title | Candidate titles |');
        lines.push('| --- | --- | --- | --- |');
        missingTemplates.forEach(finding => {
            lines.push(`| ${markdownTableCell(finding.checklistFindingId)} | ${markdownTableCell(finding.wstgId)} | ${markdownTableCell(finding.name)} | ${markdownTableCell(finding.titleCandidates.join(' / '))} |`);
        });
        lines.push('');
    }

    if (duplicateTemplateTitles.length > 0) {
        lines.push('## Duplicate Template Titles');
        lines.push('');
        lines.push('| Title | First template ID | Duplicate template ID |');
        lines.push('| --- | --- | --- |');
        duplicateTemplateTitles.forEach(duplicate => {
            lines.push(`| ${markdownTableCell(duplicate.title)} | ${markdownTableCell(duplicate.firstTemplateId)} | ${markdownTableCell(duplicate.duplicateTemplateId)} |`);
        });
        lines.push('');
    }

    await fsp.writeFile(outputPath, `${lines.join('\n')}\n`, 'utf8');
    return path.relative(ROOT_DIR, outputPath);
}

async function initTargetProject(client, config, projectName) {
    if (config.projectId) {
        const project = await client.getProject(config.projectId);
        return {
            projectId: String(project.id || config.projectId),
            projectName: String(project.name || projectName)
        };
    }

    const project = await client.createProject(projectName, config.projectDesign, config.tags);
    return {
        projectId: String(project.id),
        projectName: String(project.name || projectName)
    };
}

async function existingTemplateIds(client, projectId) {
    const findings = await client.getFindings(projectId);
    return new Set(
        findings
            .map(finding => finding && finding.template)
            .filter(Boolean)
            .map(String)
    );
}

function isSysReptorClientError(error) {
    return error instanceof AppError && error.sysreptorStatus && error.sysreptorStatus >= 400 && error.sysreptorStatus < 500;
}

async function createFromTemplateWithLanguageRetry(client, projectId, finding, config) {
    try {
        return await client.createFindingFromTemplate(projectId, finding.templateId, config.language);
    } catch (error) {
        if (!config.language || !isSysReptorClientError(error)) {
            throw error;
        }

        return client.createFindingFromTemplate(projectId, finding.templateId);
    }
}

function templateErrorDetails(error) {
    if (!(error instanceof AppError)) {
        return error instanceof Error ? error.message : String(error);
    }

    if (error.details && typeof error.details === 'object') {
        return JSON.stringify(error.details);
    }

    return error.message;
}

async function runImport(findings, config, projectName) {
    const client = new SysReptorClient({ url: config.url, token: config.token });
    const webTemplates = await client.getFindingTemplatesByTag(config.templateTag);
    const resolvedTemplates = resolveTemplatesFromTitles(findings, webTemplates);
    const missingTemplatesFile = await writeMissingTemplatesFile(
        resolvedTemplates.missingTemplates,
        config,
        projectName,
        resolvedTemplates.duplicateTemplateTitles
    );

    const target = await initTargetProject(client, config, projectName);
    const templatesAlreadyPresent = config.allowDuplicates ? new Set() : await existingTemplateIds(client, target.projectId);
    const results = [];

    for (const [index, finding] of resolvedTemplates.findings.entries()) {
        const order = index + 1;

        if (finding.templateId) {
            if (templatesAlreadyPresent.has(finding.templateId)) {
                results.push(resultFor('skipped-existing-template', 'from-template', target.projectId, target.projectName, finding));
                continue;
            }

            try {
                const created = await createFromTemplateWithLanguageRetry(client, target.projectId, finding, config);
                templatesAlreadyPresent.add(finding.templateId);
                results.push(resultFor('created', 'from-template', target.projectId, target.projectName, finding, String(created.id || '')));
                continue;
            } catch (error) {
                if (!config.fallbackOnTemplateError) {
                    results.push({
                        ...resultFor('failed-template', 'from-template', target.projectId, target.projectName, finding),
                        error: templateErrorDetails(error)
                    });
                    continue;
                }

                const created = await client.createFinding(target.projectId, buildPlaceholderPayload(finding, config, order));
                results.push({
                    ...resultFor('created-fallback', 'new-finding', target.projectId, target.projectName, finding, String(created.id || '')),
                    failedTemplateId: finding.templateId,
                    error: templateErrorDetails(error)
                });
                continue;
            }
        }

        const created = await client.createFinding(target.projectId, buildPlaceholderPayload(finding, config, order));
        results.push(resultFor('created', 'new-finding', target.projectId, target.projectName, finding, String(created.id || '')));
    }

    return {
        projectId: target.projectId,
        projectName: target.projectName,
        results,
        missingTemplates: resolvedTemplates.missingTemplates,
        missingTemplatesFile,
        duplicateTemplateTitles: resolvedTemplates.duplicateTemplateTitles,
        templatesSearched: webTemplates.length,
        templateTag: config.templateTag
    };
}

async function readJsonBody(request) {
    const chunks = [];
    let size = 0;

    for await (const chunk of request) {
        size += chunk.length;
        if (size > JSON_BODY_LIMIT) {
            throw new AppError(413, 'Request body is too large.');
        }
        chunks.push(chunk);
    }

    const text = Buffer.concat(chunks).toString('utf8');
    try {
        return JSON.parse(text || '{}');
    } catch (error) {
        throw new AppError(400, 'Request body must be valid JSON.');
    }
}

async function handleGenerateReport(request, response) {
    const body = await readJsonBody(request);
    const projectName = String(body.projectName || '').trim();
    if (!projectName) {
        throw new AppError(400, 'projectName is required.');
    }

    const findings = collectFindings(body.checklist);
    if (findings.length === 0) {
        throw new AppError(400, 'No sysreptor_findings found in the checklist payload.');
    }

    const config = getConfig();
    const importResult = await runImport(findings, config, projectName);
    const created = importResult.results.filter(result => result.status.startsWith('created')).length;
    const skipped = importResult.results.filter(result => result.status.startsWith('skipped')).length;
    const failed = importResult.results.filter(result => result.status.startsWith('failed')).length;
    const fallback = importResult.results.filter(result => result.status === 'created-fallback').length;

    sendJson(response, 200, {
        projectId: importResult.projectId,
        projectName: importResult.projectName,
        totalFindings: findings.length,
        created,
        skipped,
        failed,
        fallback,
        missingTemplates: importResult.missingTemplates.length,
        missingTemplatesFile: importResult.missingTemplatesFile,
        duplicateTemplateTitles: importResult.duplicateTemplateTitles.length,
        templatesSearched: importResult.templatesSearched,
        templateTag: importResult.templateTag,
        results: importResult.results
    });
}

async function serveStatic(request, response, pathname) {
    const requestedPath = pathname === '/' ? '/index.html' : pathname;
    const decodedPath = decodeURIComponent(requestedPath);
    const normalizedPath = path.normalize(decodedPath).replace(/^(\.\.[/\\])+/, '');
    const filePath = path.join(APP_DIR, normalizedPath);

    if (!filePath.startsWith(APP_DIR)) {
        sendJson(response, 403, { error: 'Forbidden' });
        return;
    }

    try {
        const stats = await fsp.stat(filePath);
        if (!stats.isFile()) {
            sendJson(response, 404, { error: 'Not found' });
            return;
        }

        response.writeHead(200, { 'Content-Type': contentType(filePath) });
        if (request.method === 'HEAD') {
            response.end();
            return;
        }
        fs.createReadStream(filePath).pipe(response);
    } catch {
        sendJson(response, 404, { error: 'Not found' });
    }
}

function contentType(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    return {
        '.html': 'text/html; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.json': 'application/json; charset=utf-8',
        '.webp': 'image/webp',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml; charset=utf-8'
    }[ext] || 'application/octet-stream';
}

function sendJson(response, status, payload) {
    response.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
    response.end(JSON.stringify(payload));
}

function handleError(response, error) {
    const status = error instanceof AppError ? error.status : 500;
    const message = error instanceof Error ? error.message : 'Unexpected server error.';
    const payload = { error: message };

    if (error instanceof AppError && error.details) {
        payload.details = error.details;
    }

    if (!(error instanceof AppError)) {
        console.error(error);
    }

    sendJson(response, status, payload);
}

const server = http.createServer(async (request, response) => {
    try {
        const url = new URL(request.url, `http://${request.headers.host || 'localhost'}`);

        if (request.method === 'POST' && url.pathname === '/api/sysreptor/report') {
            await handleGenerateReport(request, response);
            return;
        }

        if ((request.method === 'GET' || request.method === 'HEAD') && !url.pathname.startsWith('/api/')) {
            await serveStatic(request, response, url.pathname);
            return;
        }

        sendJson(response, 404, { error: 'Not found' });
    } catch (error) {
        handleError(response, error);
    }
});

server.listen(PORT, HOST, () => {
    console.log(`OWASP WSTG Checklist app running at http://${HOST}:${PORT}`);
});
