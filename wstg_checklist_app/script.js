window.addEventListener('error', function (e) {
    alert("JS Error: " + e.message + " at " + e.filename + ":" + e.lineno);
});
window.addEventListener('unhandledrejection', function (e) {
    alert("Unhandled Promise Rejection: " + e.reason);
});
document.addEventListener('DOMContentLoaded', () => {
    const checklistContainer = document.getElementById('checklist-container');
    const progressText = document.getElementById('progress-text');
    const progressFill = document.getElementById('progress-fill');
    const themeToggle = document.getElementById('theme-toggle-input');
    const generateSysReptorBtn = document.getElementById('generate-sysreptor-btn');
    const stateMenuContainer = document.getElementById('state-menu-container');
    const stateMenuToggle = document.getElementById('state-menu-toggle');
    const stateMenu = document.getElementById('state-menu');
    const exportBtn = document.getElementById('export-btn');
    const importBtn = document.getElementById('import-btn');
    const importFile = document.getElementById('import-file');
    const resetBtn = document.getElementById('reset-btn');
    const sysreptorDialog = document.getElementById('sysreptor-report-dialog');
    const sysreptorDialogClose = document.getElementById('sysreptor-dialog-close');
    const sysreptorDialogCancel = document.getElementById('sysreptor-dialog-cancel');
    const sysreptorReportForm = document.getElementById('sysreptor-report-form');
    const sysreptorReportTitle = document.getElementById('sysreptor-report-title');
    const sysreptorDialogStatus = document.getElementById('sysreptor-dialog-status');
    const sysreptorDialogSubmit = document.getElementById('sysreptor-dialog-submit');

    let checklistData = [];
    let state = {};
    let currentLang = localStorage.getItem('lang') || 'en';
    let previousQuery = '';
    let lastActiveCategory = '';
    let activeCategory = null;

    const i18n = {
        en: {
            header_title: "OWASP WSTG Checklist",
            header_subtitle: "Web Application Security Testing Guide Companion",
            sysreptor_generate_btn: "Generate Report",
            sysreptor_dialog_title: "Generate SysReptor Report",
            sysreptor_report_title_label: "Report title",
            sysreptor_cancel_btn: "Cancel",
            sysreptor_submit_btn: "Generate",
            state_menu_title: "Import / Export",
            export_btn: "Export State",
            import_btn: "Import State",
            reset_btn: "⚠️ Reset everything",
            progress_text: "Checked",
            status_pending: "Pending",
            status_done: "Done",
            status_finding: "Finding!",
            status_na: "N/A",
            label_information: "Information:",
            label_relevance: "Relevance",
            label_goal: "Goal / Objectives",
            label_documentation: "Documentation",
            label_summary: "Summary",
            label_methodology: "Methodology",
            label_expected_evidence: "Expected Evidence / Reporting",
            label_evidence: "Evidence:",
            label_reporting: "Reporting:",
            label_tools: "Tools",
            label_sysreptor: "SysReptor Integration",
            label_finding_title: "Finding Title (Editable):",
            label_no_content: "No content available.",
            label_no_summary: "No summary specified.",
            label_no_tools: "No specific tools mentioned.",
            btn_show_less: "▲ Show Less",
            btn_add_note: "Add Note",
            btn_add_image: "Add Image(s)",
            placeholder_notes: "Add notes (images can be pasted via Ctrl+V)...",
            alert_reset: "Warning: Do you really want to permanently delete all your progress and notes?",
            alert_import_success: "State imported successfully!",
            alert_import_zip_success: "State imported successfully from ZIP!",
            alert_import_zip_error: "Error importing ZIP file.",
            alert_import_error: "Invalid JSON file.",
            alert_export_error: "Error creating ZIP file.",
            alert_sysreptor_no_findings: "Select at least one SysReptor finding before generating a report.",
            alert_sysreptor_title_required: "Enter a report title.",
            alert_sysreptor_generating: "Generating report...",
            alert_sysreptor_success: "Report generated.",
            alert_sysreptor_error: "Could not generate the SysReptor report.",
            alert_sysreptor_server_missing: "Start the local server with npm start before generating a SysReptor report.",
            search_placeholder: "Search (e.g. WSTG, API, XSS)...",
            no_results: "No modules found matching your search."
        },
        de: {
            header_title: "OWASP WSTG Checkliste",
            header_subtitle: "Web Application Security Testing Guide Begleiter",
            sysreptor_generate_btn: "Report erstellen",
            sysreptor_dialog_title: "SysReptor Report erstellen",
            sysreptor_report_title_label: "Report-Titel",
            sysreptor_cancel_btn: "Abbrechen",
            sysreptor_submit_btn: "Erstellen",
            state_menu_title: "Import / Export",
            export_btn: "Status exportieren",
            import_btn: "Status importieren",
            reset_btn: "⚠️ Alles zurücksetzen",
            progress_text: "Geprüft",
            status_pending: "Ausstehend",
            status_done: "Erledigt",
            status_finding: "Fund!",
            status_na: "N/A",
            label_information: "Information:",
            label_relevance: "Relevanz",
            label_goal: "Ziele",
            label_documentation: "Dokumentation",
            label_summary: "Zusammenfassung",
            label_methodology: "Methodik",
            label_expected_evidence: "Erwarteter Nachweis / Berichterstattung",
            label_evidence: "Nachweis:",
            label_reporting: "Berichterstattung:",
            label_tools: "Werkzeuge",
            label_sysreptor: "SysReptor Integration",
            label_finding_title: "Titel des Befunds (Editierbar):",
            label_no_content: "Kein Inhalt verfügbar.",
            label_no_summary: "Keine Zusammenfassung angegeben.",
            label_no_tools: "Keine spezifischen Werkzeuge erwähnt.",
            btn_show_less: "▲ Weniger anzeigen",
            btn_add_note: "Hinweis hinzufügen",
            btn_add_image: "Bild(er) hinzufügen",
            placeholder_notes: "Hinweise hinzufügen (Bilder per Strg+V einfügen möglich)...",
            alert_reset: "Warnung: Möchtest du wirklich deinen gesamten Fortschritt und alle Notizen unwiderruflich löschen?",
            alert_import_success: "Status erfolgreich importiert!",
            alert_import_zip_success: "Status erfolgreich aus ZIP importiert!",
            alert_import_zip_error: "Fehler beim Importieren der ZIP-Datei.",
            alert_import_error: "Ungültige JSON-Datei.",
            alert_export_error: "Fehler beim Erstellen der ZIP-Datei.",
            alert_sysreptor_no_findings: "Wähle mindestens einen SysReptor-Befund aus, bevor ein Report erstellt wird.",
            alert_sysreptor_title_required: "Gib einen Report-Titel ein.",
            alert_sysreptor_generating: "Report wird erstellt...",
            alert_sysreptor_success: "Report wurde erstellt.",
            alert_sysreptor_error: "Der SysReptor Report konnte nicht erstellt werden.",
            alert_sysreptor_server_missing: "Starte zuerst den lokalen Server mit npm start, bevor ein SysReptor Report erstellt wird.",
            search_placeholder: "Suche (z.B. WSTG, API, XSS)...",
            no_results: "Keine passenden Module gefunden."
        }
    };

    const applyTranslations = () => {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (i18n[currentLang][key]) {
                el.textContent = i18n[currentLang][key];
            }
        });
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            if (i18n[currentLang][key]) {
                el.setAttribute('placeholder', i18n[currentLang][key]);
            }
        });
        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.getAttribute('data-i18n-title');
            if (i18n[currentLang][key]) {
                el.setAttribute('title', i18n[currentLang][key]);
            }
        });
        document.querySelectorAll('[data-i18n-aria-label]').forEach(el => {
            const key = el.getAttribute('data-i18n-aria-label');
            if (i18n[currentLang][key]) {
                el.setAttribute('aria-label', i18n[currentLang][key]);
            }
        });
    };

    const langToggleBtn = document.getElementById('lang-toggle');
    const langDropdownMenu = document.getElementById('lang-dropdown-menu');
    const langOptions = document.querySelectorAll('.lang-option');
    const langToggleFlag = langToggleBtn.querySelector('.lang-flag');

    const updateLangUI = () => {
        langOptions.forEach(opt => {
            if (opt.getAttribute('data-value') === currentLang) {
                opt.classList.add('selected');
                langToggleFlag.innerHTML = opt.querySelector('.lang-flag').innerHTML;
            } else {
                opt.classList.remove('selected');
            }
        });
    };

    const closeStateMenu = () => {
        if (stateMenu) {
            stateMenu.classList.remove('open');
        }
        if (stateMenuToggle) {
            stateMenuToggle.setAttribute('aria-expanded', 'false');
        }
    };

    const toggleStateMenu = () => {
        if (!stateMenu || !stateMenuToggle) return;
        const isOpen = !stateMenu.classList.contains('open');
        stateMenu.classList.toggle('open', isOpen);
        stateMenuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    };

    if (stateMenuToggle) {
        stateMenuToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            langDropdownMenu.classList.remove('open');
            toggleStateMenu();
        });
    }

    if (stateMenuContainer) {
        stateMenuContainer.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    langToggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        closeStateMenu();
        langDropdownMenu.classList.toggle('open');
    });

    document.addEventListener('click', () => {
        langDropdownMenu.classList.remove('open');
        closeStateMenu();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeStateMenu();
        }
    });

    langOptions.forEach(opt => {
        opt.addEventListener('click', () => {
            const newLang = opt.getAttribute('data-value');
            if (newLang !== currentLang) {
                currentLang = newLang;
                localStorage.setItem('lang', currentLang);
                updateLangUI();
                applyTranslations();
                renderChecklist();
                updateProgress();
            }
            langDropdownMenu.classList.remove('open');
        });
    });

    try {
        state = JSON.parse(localStorage.getItem('wstgState')) || {};
    } catch (e) {
        console.warn('Could not parse wstgState from localStorage', e);
    }

    // Theme Management
    const initTheme = () => {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        if (themeToggle) {
            themeToggle.checked = savedTheme === 'dark';
        }
    };

    themeToggle.addEventListener('change', (e) => {
        const newTheme = e.target.checked ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });



    // Search Functionality
    const headerRight = document.querySelector('.header-right');
    const searchInput = document.getElementById('search-input');
    const searchToggleBtn = document.getElementById('search-toggle-btn');
    const searchCloseBtn = document.getElementById('search-close-btn');

    const openSearch = () => {
        if (headerRight) {
            headerRight.classList.add('search-active');
        }
        if (searchInput) {
            searchInput.focus();
        }
    };

    const closeSearch = () => {
        if (headerRight) {
            headerRight.classList.remove('search-active');
        }
        if (searchInput) {
            searchInput.value = '';
            searchInput.blur();
        }
        renderChecklist();
    };

    if (searchToggleBtn) {
        searchToggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            closeStateMenu();
            if (headerRight && !headerRight.classList.contains('search-active')) {
                openSearch();
            }
        });
    }

    if (searchCloseBtn) {
        searchCloseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            closeSearch();
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            renderChecklist();
        });

        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeSearch();
            }
        });
    }

    // Close search if clicking outside and input is empty
    document.addEventListener('click', (e) => {
        const searchContainer = document.querySelector('.search-overlay');
        if (searchContainer && headerRight && headerRight.classList.contains('search-active')) {
            if (!searchContainer.contains(e.target) && searchInput && searchInput.value.trim() === '') {
                closeSearch();
            }
        }
    });

    // Track last active category
    if (checklistContainer) {
        const updateLastActive = (e) => {
            const categorySection = e.target.closest('.category-section');
            if (categorySection) {
                lastActiveCategory = categorySection.getAttribute('data-category');
            }
        };
        checklistContainer.addEventListener('click', updateLastActive);
        checklistContainer.addEventListener('change', updateLastActive);
        checklistContainer.addEventListener('input', updateLastActive);
    }

    // Load Data
    const loadData = () => {
        try {
            if (typeof wstgData === 'undefined') {
                throw new Error("wstgData variable is not defined. Ensure wstg_checklist_data.js is loaded.");
            }
            checklistData = wstgData;
            renderChecklist();
            updateProgress();
        } catch (error) {
            console.error(error); alert("Error: " + error.message);
            checklistContainer.innerHTML = '<p style="color: red; padding: 2rem;">Error loading checklist data. Make sure wstg_checklist_data.js exists and is loaded.</p>';
        }
    };

    // Render Logic
    const renderChecklist = () => {
        // Save current expanded state (declared below based on search status)

        const openModules = new Set(
            Array.from(checklistContainer.querySelectorAll('.module-details.open')).map(el => {
                const card = el.closest('.module-card');
                return card.getAttribute('data-id');
            })
        );

        const openDocs = new Set(
            Array.from(checklistContainer.querySelectorAll('.docs-content')).filter(el => el.style.display === 'block').map(el => {
                const card = el.closest('.module-card');
                return card.getAttribute('data-id');
            })
        );

        const openTools = new Set(
            Array.from(checklistContainer.querySelectorAll('.tools-content')).filter(el => el.style.display === 'block').map(el => {
                const card = el.closest('.module-card');
                return card.getAttribute('data-id');
            })
        );

        const query = document.getElementById('search-input')?.value.toLowerCase().trim() || '';

        let openCategories;
        if (!query && previousQuery) {
            // Collapse all except the last active category when search is cleared
            openCategories = new Set();
            if (lastActiveCategory) {
                openCategories.add(lastActiveCategory);
            }
        } else {
            openCategories = new Set(
                Array.from(checklistContainer.querySelectorAll('.category-section')).filter(s => {
                    const content = s.querySelector('.category-content');
                    return content && content.classList.contains('open');
                }).map(s => s.getAttribute('data-category'))
            );
        }

        const queryChangedToNonEmpty = query && !previousQuery;
        previousQuery = query;

        // Filter checklistData based on query
        let filteredData = checklistData;
        if (query) {
            filteredData = checklistData.filter(module => {
                const idMatch = module.id.toLowerCase().includes(query);
                const titleMatch = module.title.toLowerCase().includes(query);
                const titleDeMatch = module.title_de && module.title_de.toLowerCase().includes(query);

                return idMatch || titleMatch || titleDeMatch;
            });
        }

        checklistContainer.innerHTML = '';

        const t = i18n[currentLang];

        if (filteredData.length === 0) {
            checklistContainer.innerHTML = `
                <div class="no-results-container" style="text-align: center; padding: 4rem 1rem; color: var(--text-secondary);">
                    <svg class="no-results-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="width: 3.5rem; height: 3.5rem; margin: 0 auto 1rem auto; opacity: 0.5;">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;" data-i18n="no_results">${t.no_results}</p>
                    <p style="font-size: 0.9rem; opacity: 0.7;">${currentLang === 'de' ? 'Versuche es mit anderen Begriffen.' : 'Try adjusting your search terms.'}</p>
                </div>
            `;
            return;
        }

        // Group by category
        const categories = {};
        const categoryOrder = {};
        filteredData.forEach(module => {
            if (!categories[module.category]) {
                categories[module.category] = [];
                categoryOrder[module.category] = module.category_index || 99;
            }
            categories[module.category].push(module);
        });

        const sortedCategoryNames = Object.keys(categories).sort((a, b) => categoryOrder[a] - categoryOrder[b]);

        if (sortedCategoryNames.length > 0) {
            if (!activeCategory || !sortedCategoryNames.includes(activeCategory)) {
                activeCategory = sortedCategoryNames[0];
            }
        } else {
            activeCategory = null;
        }

        const getDisplayCategoryName = (categoryName, firstModule) => {
            let name = (currentLang === 'de' && firstModule && firstModule.category_de) ? firstModule.category_de : categoryName;
            if (currentLang === 'de' && (name === 'Tests des Konfigurations- und Bereitstellungsmanagements' || categoryName === 'Configuration and Deployment Management Testing')) {
                return 'Konfigurations - und Bereitstellungsmanagement';
            }
            return name;
        };

        // Layout creation
        const layout = document.createElement('div');
        layout.className = 'checklist-layout';

        const sidebarWrapper = document.createElement('div');
        sidebarWrapper.className = 'checklist-sidebar-wrapper';

        const sidebar = document.createElement('aside');
        sidebar.className = 'checklist-sidebar';

        const mainPanel = document.createElement('div');
        mainPanel.className = 'checklist-main-panel';

        sidebarWrapper.appendChild(sidebar);
        layout.appendChild(sidebarWrapper);
        layout.appendChild(mainPanel);
        checklistContainer.appendChild(layout);

        // Sidebar categories rendering
        if (query) {
            const searchItem = document.createElement('div');
            searchItem.className = 'sidebar-category-item active search-results-item';
            searchItem.innerHTML = `
                <div class="sidebar-category-title">🔍 ${currentLang === 'de' ? 'Suchergebnisse' : 'Search Results'}</div>
                <span class="sidebar-category-stats">${filteredData.length}</span>
            `;
            sidebar.appendChild(searchItem);

            sortedCategoryNames.forEach(categoryName => {
                const modules = categories[categoryName];
                const firstModule = modules.length > 0 ? modules[0] : null;
                const index = firstModule ? firstModule.category_index : '';
                const displayCategoryName = getDisplayCategoryName(categoryName, firstModule);

                const item = document.createElement('div');
                item.className = 'sidebar-category-item';
                item.innerHTML = `
                    <div class="sidebar-category-title">${index}. ${displayCategoryName}</div>
                    <span class="sidebar-category-stats" id="stats-${categoryName.replace(/[^a-zA-Z0-9]/g, '-')}">0 / 0</span>
                `;
                item.addEventListener('click', () => {
                    const searchInput = document.getElementById('search-input');
                    if (searchInput) searchInput.value = '';
                    const headerRight = document.querySelector('.header-right');
                    if (headerRight) headerRight.classList.remove('search-active');
                    activeCategory = categoryName;
                    renderChecklist();
                });
                sidebar.appendChild(item);
            });
        } else {
            sortedCategoryNames.forEach(categoryName => {
                const modules = categories[categoryName];
                const firstModule = modules.length > 0 ? modules[0] : null;
                const index = firstModule ? firstModule.category_index : '';
                const displayCategoryName = getDisplayCategoryName(categoryName, firstModule);

                const item = document.createElement('div');
                item.className = `sidebar-category-item ${activeCategory === categoryName ? 'active' : ''}`;
                item.innerHTML = `
                    <div class="sidebar-category-title">${index}. ${displayCategoryName}</div>
                    <span class="sidebar-category-stats" id="stats-${categoryName.replace(/[^a-zA-Z0-9]/g, '-')}">0 / 0</span>
                `;
                item.addEventListener('click', () => {
                    activeCategory = categoryName;
                    renderChecklist();
                });
                sidebar.appendChild(item);
            });
        }

        const categoriesToRender = query ? sortedCategoryNames : [activeCategory].filter(Boolean);

        for (const categoryName of categoriesToRender) {
            const modules = categories[categoryName];
            const section = document.createElement('section');
            section.className = 'category-section';
            section.setAttribute('data-category', categoryName);



            // Category Content
            const content = document.createElement('div');
            content.className = 'category-content';

            modules.forEach(module => {
                const card = document.createElement('div');
                card.className = `module-card ${openModules.has(module.id) ? 'open' : ''}`;
                card.setAttribute('data-id', module.id);

                const moduleState = state[module.id] || 'pending';

                // Content Fallback logic
                const mTitle = currentLang === 'de' && module.title_de ? module.title_de : module.title;
                const mFullText = currentLang === 'de' && module.full_text_de ? module.full_text_de : module.full_text;
                const mRelevance = currentLang === 'de' && module.relevance_de ? module.relevance_de : module.relevance;
                const mGoal = currentLang === 'de' && module.goal_de ? module.goal_de : module.goal;
                const mFullSummary = currentLang === 'de' && module.full_summary_de ? module.full_summary_de : module.full_summary;
                const mMethodology = currentLang === 'de' && module.methodology_de ? module.methodology_de : module.methodology;
                const mExpectedEvidence = currentLang === 'de' && module.expected_evidence_de ? module.expected_evidence_de : module.expected_evidence;
                const mReportingHints = currentLang === 'de' && module.reporting_hints_de ? module.reporting_hints_de : module.reporting_hints;
                const mTools = currentLang === 'de' && module.tools_de ? module.tools_de : module.tools;
                const isTop10 = (() => {
                    if (!module.id) return false;
                    if (module.id.startsWith('TOP10-') || module.id.startsWith('WSTG-APT-')) return true;
                    const exactPrefixes = ['WSTG-IDENT-', 'WSTG-ATHZ-', 'WSTG-CRYP-', 'WSTG-BUSL-', 'WSTG-CONFIG-', 'WSTG-ATHN-', 'WSTG-SESS-', 'WSTG-ERR-'];
                    if (exactPrefixes.some(prefix => module.id.startsWith(prefix))) return true;
                    const allowedInpv = ['WSTG-INPV-01', 'WSTG-INPV-02', 'WSTG-INPV-05', 'WSTG-INPV-06', 'WSTG-INPV-07', 'WSTG-INPV-11', 'WSTG-INPV-12', 'WSTG-INPV-13', 'WSTG-INPV-14'];
                    return allowedInpv.some(id => module.id.startsWith(id));
                })();

                card.innerHTML = `
                    <div class="module-header">
                        ${module.is_info ? '' : `
                        <div class="module-status" onclick="event.stopPropagation()">
                            <div class="status-icon-bar" data-id="${module.id}">
                                <button class="status-icon-btn pending ${moduleState === 'pending' ? 'active' : ''}" data-value="pending" title="${t.status_pending}" type="button">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                        <circle cx="12" cy="12" r="10"></circle>
                                        <polyline points="12 6 12 12 16 14"></polyline>
                                    </svg>
                                </button>
                                <button class="status-icon-btn done ${moduleState === 'done' ? 'active' : ''}" data-value="done" title="${t.status_done}" type="button">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                                        <polyline points="20 6 9 17 4 12"></polyline>
                                    </svg>
                                </button>
                                <button class="status-icon-btn finding ${moduleState === 'finding' ? 'active' : ''}" data-value="finding" title="${t.status_finding}" type="button">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                        <circle cx="12" cy="12" r="10"></circle>
                                        <line x1="12" y1="8" x2="12" y2="12"></line>
                                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                                    </svg>
                                </button>
                            </div>
                        </div>
                        `}
                        <div class="module-title-area">
                            ${module.is_info ?
                        `<span>ℹ️ <strong>${t.label_information}</strong> ${mTitle}</span>` :
                        `<span class="module-id" ${isTop10 ? 'title="OWASP Top 10 Module"' : ''}>${module.id}${isTop10 ? ' ⭐' : ''}</span>
                                 <span class="module-name">${mTitle}</span>`
                    }
                        </div>
                        <div class="module-arrow" style="color: var(--text-secondary);">${openModules.has(module.id) ? '▲' : '▼'}</div>
                    </div>
                    <div class="module-details ${openModules.has(module.id) ? 'open' : ''}">
                        ${module.is_info ? `
                        <div class="detail-section full-width">
                            <div class="detail-content">${marked.parse(mFullText || t.label_no_content)}</div>
                        </div>
                        ` : `
                        <div class="detail-section">
                            <h4>${t.label_relevance}</h4>
                            <div class="detail-content">${mRelevance}</div>
                        </div>
                        <div class="detail-section">
                            <h4>${t.label_goal}</h4>
                            <div class="detail-content">${marked.parse(mGoal)}</div>
                        </div>
                        <div class="detail-section full-width docs-section" style="padding: 0;">
                            <div class="docs-header" style="padding: 1rem; display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none;">
                                <h4 style="margin: 0;">${t.label_documentation}</h4>
                                <div class="docs-arrow" style="color: var(--text-secondary);">${openDocs.has(module.id) ? '▲' : '▼'}</div>
                            </div>
                            <div class="detail-content docs-content" style="display: ${openDocs.has(module.id) ? 'block' : 'none'}; padding: 0 1rem 1rem 1rem;">
                                    <h3 class="doc-section-title" style="margin-top: 0;">${t.label_summary}</h3>
                                    ${marked.parse(mFullSummary || t.label_no_summary)}
                                    
                                    <h3 class="doc-section-title">${t.label_methodology}</h3>
                                    ${marked.parse(mMethodology)}
                                    
                                    <h3 class="doc-section-title">${t.label_expected_evidence}</h3>
                                    <p><strong>${t.label_evidence}</strong> ${marked.parseInline ? marked.parseInline(mExpectedEvidence) : mExpectedEvidence}</p>
                                    <p><strong>${t.label_reporting}</strong> ${marked.parseInline ? marked.parseInline(mReportingHints) : marked.parse(mReportingHints).replace(/^<p>|<\/p>\n?$/g, '')}</p>
                                    
                                    <div style="margin-top: 1.5rem; text-align: center;">
                                        <button class="docs-close-btn btn secondary">${t.btn_show_less}</button>
                                    </div>
                            </div>
                        </div>

                        <div class="detail-section full-width tools-section" style="padding: 0;">
                            <div class="tools-header" style="padding: 1rem; display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none;">
                                <h4 style="margin: 0;">${t.label_tools}</h4>
                                <div class="tools-arrow" style="color: var(--text-secondary);">${openTools.has(module.id) ? '▲' : '▼'}</div>
                            </div>
                            <div class="detail-content tools-content" style="display: ${openTools.has(module.id) ? 'block' : 'none'}; padding: 0 1rem 1rem 1rem;">
                                    ${marked.parse(mTools || t.label_no_tools)}
                            </div>
                        </div>

                        <div class="detail-section full-width sysreptor-section" data-id="${module.id}">
                            <h4>${t.label_sysreptor}</h4>
                            <div class="detail-content">

                                <div class="sysreptor-checklist-container">
                                    <label style="font-size: 0.85rem; color: var(--text-secondary); display: block; margin-bottom: 8px;">${currentLang === 'de' ? 'Checkliste / Befunde' : 'Checklist / Findings'}:</label>
                                    <div class="sysreptor-checklist">
                                        <!-- Will be dynamically populated by renderSysReptorChecklist -->
                                    </div>
                                    <div class="sysreptor-add-custom-container" style="margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap;">
                                        <input type="text" class="sysreptor-custom-finding-input" style="flex: 1; min-width: 180px;" placeholder="${currentLang === 'de' ? 'Neuen Befund hinzufügen' : 'Add new finding'}">
                                        <input type="text" class="sysreptor-custom-uuid-input" style="width: 250px;" placeholder="SysReptor ID (optional)">
                                        <button class="sysreptor-add-custom-btn">${currentLang === 'de' ? 'Hinzufügen' : 'Add'}</button>
                                    </div>
                                </div>

                                <div class="sysreptor-notes-container">
                                    <label style="font-size: 0.85rem; color: var(--text-secondary); display: block; margin-top: 4px; margin-bottom: 0;">${currentLang === 'de' ? 'Zusätzliche Hinweise & Medien' : 'Additional Notes & Media'}:</label>
                                    <ul class="sysreptor-notes-list"></ul>
                                    <div class="sysreptor-images-list" style="margin-bottom: 10px; margin-top: 5px;"></div>
                                    <textarea class="sysreptor-note-textarea" placeholder="${t.placeholder_notes}"></textarea>
                                    <div style="display: flex; gap: 10px; margin-top: 5px;">
                                        <button class="sysreptor-add-note-btn">${t.btn_add_note}</button>
                                        <button class="sysreptor-add-image-btn btn secondary" style="padding: 6px 12px; font-size: 0.85rem;">${t.btn_add_image}</button>
                                    </div>
                                    <input type="file" class="sysreptor-image-input" accept="image/*" multiple style="display: none;">
                                </div>
                            </div>
                        </div>
                        `}
                    </div>
                `;

                // Header Click -> Toggle details
                const modHeader = card.querySelector('.module-header');
                const modDetails = card.querySelector('.module-details');
                modHeader.addEventListener('click', () => {
                    if (modDetails.classList.contains('open')) {
                        modDetails.classList.remove('open');
                        card.classList.remove('open');
                        const arrow = modHeader.querySelector('.module-arrow');
                        arrow.textContent = '▼';
                    } else {
                        modDetails.classList.add('open');
                        card.classList.add('open');
                        const arrow = modHeader.querySelector('.module-arrow');
                        arrow.textContent = '▲';

                        // Scroll module into view smoothly inside the container
                        setTimeout(() => {
                            const container = card.closest('.category-content');
                            if (container) {
                                const containerRect = container.getBoundingClientRect();
                                const cardRect = card.getBoundingClientRect();
                                const targetScrollTop = container.scrollTop + (cardRect.top - containerRect.top) - 16;
                                container.scrollTo({ top: targetScrollTop, behavior: 'smooth' });
                            }
                        }, 50);
                    }
                });

                // Documentation expand logic
                const docsHeader = card.querySelector('.docs-header');
                const docsContent = card.querySelector('.docs-content');
                const docsArrow = card.querySelector('.docs-arrow');
                const docsCloseBtn = card.querySelector('.docs-close-btn');

                const toggleDocs = (scrollToTop = false) => {
                    if (docsContent.style.display === 'none') {
                        docsContent.style.display = 'block';
                        docsArrow.textContent = '▲';
                    } else {
                        let targetScrollTop = 0;
                        const container = card.closest('.category-content');
                        if (scrollToTop && container) {
                            const containerRect = container.getBoundingClientRect();
                            const cardRect = card.getBoundingClientRect();
                            targetScrollTop = container.scrollTop + (cardRect.top - containerRect.top) - 16;
                        }

                        docsContent.style.display = 'none';
                        docsArrow.textContent = '▼';

                        if (scrollToTop && container) {
                            setTimeout(() => {
                                container.scrollTo({ top: targetScrollTop, behavior: 'smooth' });
                            }, 10);
                        }
                    }
                };

                if (docsHeader) {
                    docsHeader.addEventListener('click', (e) => {
                        e.stopPropagation();
                        toggleDocs(false); // No scroll needed when clicking the top header
                    });
                }
                if (docsCloseBtn) {
                    docsCloseBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        toggleDocs(true); // Scroll up when clicking the bottom close button
                    });
                }

                // Tools expand logic
                const toolsHeader = card.querySelector('.tools-header');
                const toolsContent = card.querySelector('.tools-content');
                const toolsArrow = card.querySelector('.tools-arrow');

                const toggleTools = () => {
                    if (!toolsContent) return;
                    if (toolsContent.style.display === 'none') {
                        toolsContent.style.display = 'block';
                        toolsArrow.textContent = '▲';
                    } else {
                        toolsContent.style.display = 'none';
                        toolsArrow.textContent = '▼';
                    }
                };

                if (toolsHeader) {
                    toolsHeader.addEventListener('click', (e) => {
                        e.stopPropagation();
                        toggleTools();
                    });
                }

                // Status Change
                if (!module.is_info) {
                    const iconBtns = card.querySelectorAll('.status-icon-btn');
                    iconBtns.forEach(btn => {
                        btn.addEventListener('click', () => {
                            const newVal = btn.getAttribute('data-value');
                            state[module.id] = newVal;

                            // Update active states
                            iconBtns.forEach(b => {
                                if (b.getAttribute('data-value') === newVal) {
                                    b.classList.add('active');
                                } else {
                                    b.classList.remove('active');
                                }
                            });

                            saveState();
                            updateProgress();
                        });
                    });

                    // SysReptor Logic
                    const textarea = card.querySelector('.sysreptor-note-textarea');
                    const addBtn = card.querySelector('.sysreptor-add-note-btn');
                    const notesList = card.querySelector('.sysreptor-notes-list');

                    if (!textarea || !addBtn || !notesList) {
                        console.error("SysReptor fields missing for module:", module.id);
                        return; // skip event listeners for this card
                    }

                    // SysReptor Checklist Render and Event Listeners
                    const renderSysReptorChecklist = () => {
                        const checklistEl = card.querySelector('.sysreptor-checklist');
                        if (!checklistEl) return;

                        const mFindings = state[module.id + '_sysreptor_findings'] || {};

                        // Predefined templates
                        let html = (module.sysreptor_templates || []).map(tmpl => {
                            const fData = mFindings[tmpl.id] || {};
                            const isChecked = !!fData.checked;
                            const title = currentLang === 'de' ? tmpl.title_de : tmpl.title_en;
                            const sysreptorIdVal = tmpl.sysreptor_id || '';
                            const tooltipText = sysreptorIdVal ? `SysReptor ID: ${sysreptorIdVal}` : 'SysReptor';
                            const sysreptorIconHtml = `
                            <span class="sysreptor-icon-container" data-tooltip="${tooltipText}" data-sysreptor-id="${sysreptorIdVal}">
                                <svg class="sysreptor-icon" viewBox="0 0 100 100" fill="currentColor" style="width: 16px; height: 16px; margin-left: 8px; vertical-align: middle; cursor: pointer; color: var(--text-secondary);">
                                    <path d="M 10,16 C 25,11 75,10 93,31 C 80,34 30,34 10,24 C 8,22 8,18 10,16 Z" />
                                    <path d="M 10,46 C 25,41 75,40 93,61 C 80,64 30,64 10,54 C 8,52 8,48 10,46 Z" />
                                    <path d="M 12,73 C 27,68 77,67 95,88 C 82,91 32,91 12,81 C 10,79 10,75 12,73 Z" />
                                </svg>
                            </span>`;
                            return `
                            <div class="sysreptor-finding-card ${isChecked ? 'checked' : ''}" data-finding-id="${tmpl.id}">
                                <div class="sysreptor-finding-header">
                                    <div class="sysreptor-finding-header-left" style="display: flex; align-items: center; flex-wrap: wrap;">
                                        <input type="checkbox" class="sysreptor-finding-checkbox" ${isChecked ? 'checked' : ''}>
                                        <span class="sysreptor-finding-title">${title.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</span>
                                    </div>
                                    ${sysreptorIconHtml}
                                </div>
                            </div>
                            `;
                        }).join('');

                        // Custom findings
                        html += Object.entries(mFindings)
                            .filter(([fid, fData]) => fData && fData.is_custom)
                            .map(([fid, fData]) => {
                                const isChecked = !!fData.checked;
                                const title = fData.title || '';
                                const sysreptorIdVal = fData.sysreptor_id || '';
                                const tooltipText = sysreptorIdVal ? `SysReptor ID: ${sysreptorIdVal}` : 'SysReptor';
                                const sysreptorIconHtml = `
                                <span class="sysreptor-icon-container" data-tooltip="${tooltipText}" data-sysreptor-id="${sysreptorIdVal}">
                                    <svg class="sysreptor-icon" viewBox="0 0 100 100" fill="currentColor" style="width: 16px; height: 16px; margin-left: 8px; vertical-align: middle; cursor: pointer; color: var(--text-secondary);">
                                        <path d="M 10,16 C 25,11 75,10 93,31 C 80,34 30,34 10,24 C 8,22 8,18 10,16 Z" />
                                        <path d="M 10,46 C 25,41 75,40 93,61 C 80,64 30,64 10,54 C 8,52 8,48 10,46 Z" />
                                        <path d="M 12,73 C 27,68 77,67 95,88 C 82,91 32,91 12,81 C 10,79 10,75 12,73 Z" />
                                    </svg>
                                </span>`;
                                return `
                                <div class="sysreptor-finding-card ${isChecked ? 'checked' : ''} custom-finding" data-finding-id="${fid}">
                                    <div class="sysreptor-finding-header">
                                        <div class="sysreptor-finding-header-left" style="display: flex; align-items: center; flex-wrap: wrap;">
                                            <input type="checkbox" class="sysreptor-finding-checkbox" ${isChecked ? 'checked' : ''}>
                                            <span class="sysreptor-finding-title">${title.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</span>
                                        </div>
                                        <div style="display: flex; align-items: center; gap: 8px;">
                                            ${sysreptorIconHtml}
                                            <button class="sysreptor-finding-delete-btn" type="button" style="background: none; border: none; color: var(--text-secondary); cursor: pointer; padding: 4px 8px; font-size: 1.1rem; line-height: 1;">&times;</button>
                                        </div>
                                    </div>
                                </div>
                                `;
                            }).join('');

                        checklistEl.innerHTML = html;

                        // Bind events
                        const findingCards = checklistEl.querySelectorAll('.sysreptor-finding-card');
                        findingCards.forEach(fCard => {
                            const findingId = fCard.getAttribute('data-finding-id');
                            const checkbox = fCard.querySelector('.sysreptor-finding-checkbox');
                            const deleteBtn = fCard.querySelector('.sysreptor-finding-delete-btn');
                            const iconContainer = fCard.querySelector('.sysreptor-icon-container');

                            const getFindingState = () => {
                                if (!state[module.id + '_sysreptor_findings']) {
                                    state[module.id + '_sysreptor_findings'] = {};
                                }
                                if (!state[module.id + '_sysreptor_findings'][findingId]) {
                                    state[module.id + '_sysreptor_findings'][findingId] = {};
                                }
                                return state[module.id + '_sysreptor_findings'][findingId];
                            };

                            checkbox.addEventListener('change', (e) => {
                                const fState = getFindingState();
                                fState.checked = e.target.checked;
                                if (e.target.checked) {
                                    fCard.classList.add('checked');
                                } else {
                                    fCard.classList.remove('checked');
                                }
                                saveState();
                            });

                            fCard.addEventListener('click', (e) => {
                                if (e.target.closest('.sysreptor-finding-checkbox')) {
                                    return;
                                }
                                if (e.target.closest('.sysreptor-finding-delete-btn') || e.target.closest('.sysreptor-icon-container')) {
                                    return;
                                }
                                checkbox.checked = !checkbox.checked;
                                const fState = getFindingState();
                                fState.checked = checkbox.checked;
                                if (checkbox.checked) {
                                    fCard.classList.add('checked');
                                } else {
                                    fCard.classList.remove('checked');
                                }
                                saveState();
                            });

                            if (iconContainer) {
                                iconContainer.addEventListener('click', (e) => {
                                    e.stopPropagation();
                                    const id = iconContainer.getAttribute('data-sysreptor-id');
                                    if (id) {
                                        navigator.clipboard.writeText(id).then(() => {
                                            const originalTooltip = iconContainer.getAttribute('data-tooltip');
                                            iconContainer.setAttribute('data-tooltip', currentLang === 'de' ? 'Kopiert!' : 'Copied!');
                                            setTimeout(() => {
                                                iconContainer.setAttribute('data-tooltip', originalTooltip);
                                            }, 2000);
                                        }).catch(err => {
                                            console.error('Could not copy text: ', err);
                                        });
                                    }
                                });
                            }

                            if (deleteBtn) {
                                deleteBtn.addEventListener('click', (e) => {
                                    e.stopPropagation();
                                    if (state[module.id + '_sysreptor_findings']) {
                                        delete state[module.id + '_sysreptor_findings'][findingId];
                                        saveState();
                                        renderSysReptorChecklist();
                                    }
                                });
                            }
                        });
                    };


                    const addCustomInput = card.querySelector('.sysreptor-custom-finding-input');
                    const addCustomUuidInput = card.querySelector('.sysreptor-custom-uuid-input');
                    const addCustomBtn = card.querySelector('.sysreptor-add-custom-btn');

                    if (addCustomInput && addCustomBtn) {
                        const addCustomFinding = () => {
                            const title = addCustomInput.value.trim();
                            if (!title) return;
                            const uuid = addCustomUuidInput ? addCustomUuidInput.value.trim() : '';

                            const fid = 'custom_' + Date.now();
                            if (!state[module.id + '_sysreptor_findings']) {
                                state[module.id + '_sysreptor_findings'] = {};
                            }
                            state[module.id + '_sysreptor_findings'][fid] = {
                                checked: true,
                                title: title,
                                is_custom: true
                            };
                            if (uuid) {
                                state[module.id + '_sysreptor_findings'][fid].sysreptor_id = uuid;
                            }

                            saveState();
                            addCustomInput.value = '';
                            if (addCustomUuidInput) addCustomUuidInput.value = '';
                            renderSysReptorChecklist();
                        };

                        addCustomBtn.addEventListener('click', addCustomFinding);
                        addCustomInput.addEventListener('keydown', (e) => {
                            if (e.key === 'Enter') {
                                e.preventDefault();
                                addCustomFinding();
                            }
                        });
                        if (addCustomUuidInput) {
                            addCustomUuidInput.addEventListener('keydown', (e) => {
                                if (e.key === 'Enter') {
                                    e.preventDefault();
                                    addCustomFinding();
                                }
                            });
                        }
                    }

                    renderSysReptorChecklist();

                    const renderNotes = () => {
                        const notes = state[module.id + '_notes'] || [];
                        notesList.innerHTML = notes.map((note, idx) => `
                            <li class="sysreptor-note-item" data-index="${idx}">
                                <span class="sysreptor-note-text">${note.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</span>
                                <button class="sysreptor-note-delete" title="Löschen">✕</button>
                            </li>
                        `).join('');

                        notesList.querySelectorAll('.sysreptor-note-delete').forEach(delBtn => {
                            delBtn.addEventListener('click', (e) => {
                                const li = e.target.closest('li');
                                const idx = parseInt(li.getAttribute('data-index'));
                                notes.splice(idx, 1);
                                state[module.id + '_notes'] = notes;
                                saveState();
                                renderNotes();
                            });
                        });
                    };

                    renderNotes();

                    addBtn.addEventListener('click', () => {
                        const text = textarea.value.trim();
                        if (text) {
                            const notes = state[module.id + '_notes'] || [];
                            notes.push(text);
                            state[module.id + '_notes'] = notes;
                            saveState();
                            textarea.value = '';
                            renderNotes();
                        }
                    });

                    // Handle paste event for images
                    textarea.addEventListener('paste', (e) => {
                        const items = (e.clipboardData || window.clipboardData).items;
                        for (let index in items) {
                            const item = items[index];
                            if (item.kind === 'file' && item.type.startsWith('image/')) {
                                const blob = item.getAsFile();
                                const reader = new FileReader();
                                reader.onload = (event) => {
                                    const images = state[module.id + '_images'] || [];
                                    images.push(event.target.result);
                                    state[module.id + '_images'] = images;
                                    saveState();
                                    if (typeof renderImages === 'function') {
                                        renderImages();
                                    }
                                };
                                reader.readAsDataURL(blob);
                            }
                        }
                    });

                    // Image Logic
                    const imageInput = card.querySelector('.sysreptor-image-input');
                    const addImageBtn = card.querySelector('.sysreptor-add-image-btn');
                    const imagesList = card.querySelector('.sysreptor-images-list');

                    if (addImageBtn && imageInput) {
                        addImageBtn.addEventListener('click', () => {
                            imageInput.click();
                        });

                        imageInput.addEventListener('change', (e) => {
                            const files = e.target.files;
                            if (!files || files.length === 0) return;

                            const images = state[module.id + '_images'] || [];

                            Array.from(files).forEach(file => {
                                const reader = new FileReader();
                                reader.onload = (event) => {
                                    images.push(event.target.result);
                                    state[module.id + '_images'] = images;
                                    saveState();
                                    renderImages();
                                };
                                reader.readAsDataURL(file);
                            });

                            imageInput.value = '';
                        });
                    }

                    const renderImages = () => {
                        const images = state[module.id + '_images'] || [];
                        imagesList.innerHTML = images.map((imgData, idx) => `
                            <div class="sysreptor-image-wrapper" style="position: relative; display: inline-block;">
                                <img src="${imgData}" class="sysreptor-preview-img" data-index="${idx}" alt="Preview" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px; cursor: pointer; border: 1px solid var(--border-color);">
                                <button class="sysreptor-image-delete" data-index="${idx}" style="position: absolute; top: -5px; right: -5px; background: #ef4444; color: white; border: none; border-radius: 50%; width: 20px; height: 20px; cursor: pointer; font-size: 12px; line-height: 1; display: flex; align-items: center; justify-content: center;">✕</button>
                            </div>
                        `).join('');

                        imagesList.querySelectorAll('.sysreptor-image-delete').forEach(delBtn => {
                            delBtn.addEventListener('click', (e) => {
                                e.stopPropagation();
                                const idx = parseInt(e.target.getAttribute('data-index'));
                                const imgs = state[module.id + '_images'] || [];
                                imgs.splice(idx, 1);
                                state[module.id + '_images'] = imgs;
                                saveState();
                                renderImages();
                            });
                        });

                        imagesList.querySelectorAll('.sysreptor-preview-img').forEach(img => {
                            img.addEventListener('click', (e) => {
                                if (window.openImageModal) window.openImageModal(e.target.src);
                            });
                        });
                    };

                    if (imagesList) {
                        renderImages();
                    }
                }

                content.appendChild(card);
            });

            // Toggle Category Content
            content.classList.add('open');

            section.appendChild(content);
            mainPanel.appendChild(section);
        }
        updateProgress();
    };

    const updateProgress = () => {
        let completed = 0;
        let total = 0;

        // Also update category stats
        const categoryCounts = {};
        checklistData.forEach(module => {
            if (module.is_info) return;

            total++;
            if (!categoryCounts[module.category]) categoryCounts[module.category] = { total: 0, done: 0 };
            categoryCounts[module.category].total++;

            const moduleState = state[module.id];
            if (moduleState && moduleState !== 'pending') {
                completed++;
                categoryCounts[module.category].done++;
            }
        });

        const t = i18n[currentLang];
        progressText.textContent = `${completed} / ${total} ${t.progress_text}`;
        const percentage = total === 0 ? 0 : (completed / total) * 100;
        progressFill.style.width = `${percentage}%`;

        for (const [cat, counts] of Object.entries(categoryCounts)) {
            const statsEl = document.getElementById(`stats-${cat.replace(/[^a-zA-Z0-9]/g, '-')}`);
            if (statsEl) {
                statsEl.textContent = `${counts.done} / ${counts.total}`;
            }
        }
    };

    const saveState = () => {
        localStorage.setItem('wstgState', JSON.stringify(state));
    };

    const buildExportData = ({ includeImages = true } = {}) => {
        const exportData = {};

        checklistData.forEach(module => {
            if (module.is_info) return;

            const status = state[module.id] || 'pending';
            const title = state[module.id + '_title'];
            const notes = state[module.id + '_notes'];
            const images = state[module.id + '_images'];

            const mFindings = state[module.id + '_sysreptor_findings'] || {};
            const hasCheckedFindings = Object.values(mFindings).some(f => f && f.checked);

            if (status !== 'pending' || title || (notes && notes.length > 0) || (includeImages && images && images.length > 0) || hasCheckedFindings) {
                exportData[module.id] = {
                    status: status,
                    title: title || (currentLang === 'de' ? (module.title_de || module.title) : module.title)
                };
                if (notes && notes.length > 0) {
                    exportData[module.id].notes = notes;
                }

                if (hasCheckedFindings) {
                    const checkedFindings = [];
                    let findingCounter = 1;

                    (module.sysreptor_templates || []).forEach(tmpl => {
                        const fState = mFindings[tmpl.id];
                        if (fState && fState.checked) {
                            const findingObj = {
                                id: `${module.id}-${findingCounter}`,
                                name: currentLang === 'de' ? tmpl.title_de : tmpl.title_en,
                                title_en: tmpl.title_en,
                                title_de: tmpl.title_de
                            };
                            if (tmpl.sysreptor_id) {
                                findingObj.sysreptor_id = tmpl.sysreptor_id;
                            }
                            checkedFindings.push(findingObj);
                        }
                        findingCounter++;
                    });

                    Object.entries(mFindings)
                        .filter(([, fState]) => fState && fState.is_custom && fState.checked)
                        .forEach(([, fState]) => {
                            const findingObj = {
                                id: `${module.id}-${findingCounter}`,
                                name: fState.title || ''
                            };
                            if (fState.sysreptor_id) {
                                findingObj.sysreptor_id = fState.sysreptor_id;
                            }
                            checkedFindings.push(findingObj);
                            findingCounter++;
                        });

                    if (checkedFindings.length > 0) {
                        exportData[module.id].sysreptor_findings = checkedFindings;
                    }
                }

                if (includeImages && images && images.length > 0) {
                    exportData[module.id].images = [];
                    images.forEach((imgData, idx) => {
                        const mimeMatch = imgData.match(/data:([a-zA-Z0-9]+\/[a-zA-Z0-9-.+]+).*,.*/);
                        let ext = "png";
                        if (mimeMatch && mimeMatch.length > 1) {
                            const mime = mimeMatch[1];
                            if (mime === "image/jpeg") ext = "jpg";
                            else if (mime === "image/gif") ext = "gif";
                            else if (mime === "image/webp") ext = "webp";
                        }
                        exportData[module.id].images.push(`${module.id}_${idx}.${ext}`);
                    });
                }
            }
        });

        return exportData;
    };

    const addImagesToZip = (zip, exportData) => {
        const imagesFolder = zip.folder("images");

        checklistData.forEach(module => {
            const imageNames = exportData[module.id]?.images;
            if (!imageNames || imageNames.length === 0) return;

            const images = state[module.id + '_images'] || [];
            images.forEach((imgData, idx) => {
                const fileName = imageNames[idx];
                if (!fileName) return;

                const base64Data = imgData.split(',')[1];
                if (base64Data) {
                    imagesFolder.file(fileName, base64Data, { base64: true });
                }
            });
        });
    };

    const countSysReptorFindings = (exportData) => Object.values(exportData).reduce((total, moduleData) => {
        if (!moduleData || !Array.isArray(moduleData.sysreptor_findings)) return total;
        return total + moduleData.sysreptor_findings.length;
    }, 0);

    const setSysReptorDialogStatus = (message, type = '') => {
        if (!sysreptorDialogStatus) return;

        sysreptorDialogStatus.className = `sysreptor-dialog-status ${type}`.trim();
        sysreptorDialogStatus.textContent = message || '';
    };

    const setSysReptorDialogSuccess = (data) => {
        if (!sysreptorDialogStatus) return;

        sysreptorDialogStatus.className = 'sysreptor-dialog-status success';
        sysreptorDialogStatus.textContent = '';

        const summary = document.createElement('span');
        const fallbackText = data.fallback ? `, ${data.fallback} fallback` : '';
        const failedText = data.failed ? `, ${data.failed} failed` : '';
        const missingText = data.missingTemplates ? `, ${data.missingTemplates} missing template${data.missingTemplates === 1 ? '' : 's'}` : '';
        summary.textContent = `${i18n[currentLang].alert_sysreptor_success} ${data.projectName || ''} (${data.projectId || ''}). ${data.created || 0} created, ${data.skipped || 0} skipped${fallbackText}${failedText}${missingText}.`;
        sysreptorDialogStatus.appendChild(summary);

        if (data.missingTemplates && data.missingTemplatesFile) {
            const missingInfo = document.createElement('span');
            missingInfo.textContent = ` Missing list: ${data.missingTemplatesFile}.`;
            sysreptorDialogStatus.appendChild(document.createTextNode(' '));
            sysreptorDialogStatus.appendChild(missingInfo);
        }

        if (data.projectUrl) {
            const link = document.createElement('a');
            link.href = data.projectUrl;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            link.textContent = currentLang === 'de' ? 'In SysReptor öffnen' : 'Open in SysReptor';
            sysreptorDialogStatus.appendChild(document.createTextNode(' '));
            sysreptorDialogStatus.appendChild(link);
        }
    };

    const openSysReptorDialog = () => {
        if (!sysreptorDialog || !sysreptorReportTitle) return;

        const defaultTitle = localStorage.getItem('sysreptorReportTitle') || 'OWASP WSTG Checklist Report';
        sysreptorReportTitle.value = defaultTitle;
        setSysReptorDialogStatus('');
        sysreptorDialog.classList.add('open');
        sysreptorDialog.setAttribute('aria-hidden', 'false');
        setTimeout(() => {
            sysreptorReportTitle.focus();
            sysreptorReportTitle.select();
        }, 0);
    };

    const closeSysReptorDialog = () => {
        if (!sysreptorDialog) return;
        sysreptorDialog.classList.remove('open');
        sysreptorDialog.setAttribute('aria-hidden', 'true');
    };

    if (generateSysReptorBtn) {
        generateSysReptorBtn.addEventListener('click', openSysReptorDialog);
    }

    if (sysreptorDialogClose) {
        sysreptorDialogClose.addEventListener('click', closeSysReptorDialog);
    }

    if (sysreptorDialogCancel) {
        sysreptorDialogCancel.addEventListener('click', closeSysReptorDialog);
    }

    if (sysreptorDialog) {
        sysreptorDialog.addEventListener('click', (e) => {
            if (e.target === sysreptorDialog) {
                closeSysReptorDialog();
            }
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && sysreptorDialog && sysreptorDialog.classList.contains('open')) {
            closeSysReptorDialog();
        }
    });

    if (sysreptorReportForm) {
        sysreptorReportForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const projectName = sysreptorReportTitle ? sysreptorReportTitle.value.trim() : '';
            if (!projectName) {
                setSysReptorDialogStatus(i18n[currentLang].alert_sysreptor_title_required, 'error');
                return;
            }

            const checklist = buildExportData({ includeImages: false });
            const findingCount = countSysReptorFindings(checklist);
            if (findingCount === 0) {
                setSysReptorDialogStatus(i18n[currentLang].alert_sysreptor_no_findings, 'error');
                return;
            }

            localStorage.setItem('sysreptorReportTitle', projectName);
            setSysReptorDialogStatus(i18n[currentLang].alert_sysreptor_generating, 'loading');

            if (sysreptorDialogSubmit) {
                sysreptorDialogSubmit.disabled = true;
            }

            try {
                const response = await fetch('/api/sysreptor/report', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        projectName,
                        checklist
                    })
                });

                let responseData = {};
                try {
                    responseData = await response.json();
                } catch (parseError) {
                    responseData = {};
                }

                if (!response.ok) {
                    const message = responseData.error || responseData.message || i18n[currentLang].alert_sysreptor_error;
                    throw new Error(message);
                }

                setSysReptorDialogSuccess(responseData);
            } catch (err) {
                const message = err instanceof TypeError
                    ? i18n[currentLang].alert_sysreptor_server_missing
                    : (err.message || i18n[currentLang].alert_sysreptor_error);
                setSysReptorDialogStatus(message, 'error');
            } finally {
                if (sysreptorDialogSubmit) {
                    sysreptorDialogSubmit.disabled = false;
                }
            }
        });
    }

    // Export/Import State
    exportBtn.addEventListener('click', async () => {
        closeStateMenu();
        const exportData = buildExportData();
        const zip = new JSZip();
        addImagesToZip(zip, exportData);

        zip.file("wstg_pentest_state.json", JSON.stringify(exportData, null, 2));

        try {
            const content = await zip.generateAsync({ type: "blob" });
            const url = URL.createObjectURL(content);
            const downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href", url);
            downloadAnchorNode.setAttribute("download", "wstg_pentest_state.zip");
            document.body.appendChild(downloadAnchorNode);
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
            URL.revokeObjectURL(url);
        } catch (e) {
            console.error("Failed to generate zip", e);
            alert(i18n[currentLang].alert_export_error);
        }
    });

    importBtn.addEventListener('click', () => {
        closeStateMenu();
        importFile.click();
    });

    importFile.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const parseImportedFindings = (findings, moduleId) => {
            const mFindings = {};
            const module = checklistData.find(m => m.id === moduleId);
            (findings || []).forEach(f => {
                let fid = f.id;
                let title = f.name || f.title_custom || '';
                let isCustom = false;

                // Check if it's new format "ModuleID-Number"
                const match = f.id.match(new RegExp(`^${moduleId}-(\\d+)$`));
                if (match) {
                    const index = parseInt(match[1], 10) - 1;
                    const templates = module ? module.sysreptor_templates : [];
                    if (templates && index >= 0 && index < templates.length) {
                        fid = templates[index].id;
                    } else {
                        isCustom = true;
                    }
                } else if (f.id.startsWith('custom_')) {
                    isCustom = true;
                }

                mFindings[fid] = {
                    checked: true
                };
                if (isCustom) {
                    mFindings[fid].is_custom = true;
                    mFindings[fid].title = title;
                    if (f.sysreptor_id) {
                        mFindings[fid].sysreptor_id = f.sysreptor_id;
                    }
                }
            });
            return mFindings;
        };

        if (file.name.endsWith('.zip')) {
            try {
                const zip = await JSZip.loadAsync(file);
                const jsonFile = zip.file("wstg_pentest_state.json");
                if (!jsonFile) throw new Error("Missing wstg_pentest_state.json in zip");

                const jsonContent = await jsonFile.async("string");
                const importedData = JSON.parse(jsonContent);
                const newState = {};

                for (const key in importedData) {
                    if (typeof importedData[key] === 'object' && !Array.isArray(importedData[key])) {
                        newState[key] = importedData[key].status || 'pending';
                        if (importedData[key].title) {
                            newState[key + '_title'] = importedData[key].title;
                        }
                        if (importedData[key].notes) {
                            newState[key + '_notes'] = importedData[key].notes;
                        }
                        if (importedData[key].sysreptor_findings) {
                            newState[key + '_sysreptor_findings'] = parseImportedFindings(importedData[key].sysreptor_findings, key);
                        }
                        if (importedData[key].images) {
                            const images = [];
                            for (const fileName of importedData[key].images) {
                                // Fallback to handle old export format where image was base64 directly
                                if (fileName.startsWith('data:image/')) {
                                    images.push(fileName);
                                    continue;
                                }
                                const imgFile = zip.file(`images/${fileName}`);
                                if (imgFile) {
                                    const base64Data = await imgFile.async("base64");
                                    let mime = "image/png";
                                    if (fileName.endsWith('.jpg') || fileName.endsWith('.jpeg')) mime = "image/jpeg";
                                    else if (fileName.endsWith('.gif')) mime = "image/gif";
                                    else if (fileName.endsWith('.webp')) mime = "image/webp";
                                    images.push(`data:${mime};base64,${base64Data}`);
                                }
                            }
                            if (images.length > 0) {
                                newState[key + '_images'] = images;
                            }
                        }
                    } else {
                        newState[key] = importedData[key];
                    }
                }

                state = newState;
                saveState();
                renderChecklist();
                updateProgress();
                alert(i18n[currentLang].alert_import_zip_success);
            } catch (err) {
                console.error(err);
                alert(i18n[currentLang].alert_import_zip_error);
            }
        } else {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const importedData = JSON.parse(e.target.result);
                    const newState = {};

                    for (const key in importedData) {
                        if (typeof importedData[key] === 'object' && !Array.isArray(importedData[key])) {
                            newState[key] = importedData[key].status || 'pending';
                            if (importedData[key].title) {
                                newState[key + '_title'] = importedData[key].title;
                            }
                            if (importedData[key].notes) {
                                newState[key + '_notes'] = importedData[key].notes;
                            }
                            if (importedData[key].sysreptor_findings) {
                                newState[key + '_sysreptor_findings'] = parseImportedFindings(importedData[key].sysreptor_findings, key);
                            }
                            if (importedData[key].images) {
                                newState[key + '_images'] = importedData[key].images;
                            }
                        } else {
                            newState[key] = importedData[key];
                        }
                    }

                    state = newState;
                    saveState();
                    renderChecklist();
                    updateProgress();
                    alert(i18n[currentLang].alert_import_success);
                } catch (err) {
                    alert(i18n[currentLang].alert_import_error);
                }
            };
            reader.readAsText(file);
        }
        importFile.value = '';
    });

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            const confirmed = confirm(i18n[currentLang].alert_reset);
            if (confirmed) {
                state = {};
                saveState();
                renderChecklist();
                updateProgress();
            }
        });
    }

    // Image Modal Logic
    const imageModal = document.createElement('div');
    imageModal.className = 'image-modal';
    imageModal.innerHTML = `
        <div class="image-modal-backdrop"></div>
        <img class="image-modal-content" src="">
        <button class="image-modal-close">✕</button>
    `;
    document.body.appendChild(imageModal);

    window.openImageModal = (src) => {
        imageModal.querySelector('.image-modal-content').src = src;
        imageModal.classList.add('open');
    };

    imageModal.querySelector('.image-modal-backdrop').addEventListener('click', () => {
        imageModal.classList.remove('open');
    });
    imageModal.querySelector('.image-modal-close').addEventListener('click', () => {
        imageModal.classList.remove('open');
    });

    // Init
    initTheme();
    updateLangUI();
    applyTranslations();
    loadData();
});
