window.addEventListener('error', function(e) {
    alert("JS Error: " + e.message + " at " + e.filename + ":" + e.lineno);
});
window.addEventListener('unhandledrejection', function(e) {
    alert("Unhandled Promise Rejection: " + e.reason);
});
document.addEventListener('DOMContentLoaded', () => {
    const checklistContainer = document.getElementById('checklist-container');
    const progressText = document.getElementById('progress-text');
    const progressFill = document.getElementById('progress-fill');
    const themeToggle = document.getElementById('theme-toggle');
    const exportBtn = document.getElementById('export-btn');
    const importBtn = document.getElementById('import-btn');
    const importFile = document.getElementById('import-file');
    const resetBtn = document.getElementById('reset-btn');

    let checklistData = [];
    let state = {};
    try {
        state = JSON.parse(localStorage.getItem('wstgState')) || {};
    } catch (e) {
        console.warn('Could not parse wstgState from localStorage', e);
    }

    // Theme Management
    const initTheme = () => {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
    };

    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });

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
        checklistContainer.innerHTML = '';
        
        // Group by category
        const categories = {};
        const categoryOrder = {};
        checklistData.forEach(module => {
            if (!categories[module.category]) {
                categories[module.category] = [];
                categoryOrder[module.category] = module.category_index || 99;
            }
            categories[module.category].push(module);
        });

        const sortedCategoryNames = Object.keys(categories).sort((a, b) => categoryOrder[a] - categoryOrder[b]);

        for (const categoryName of sortedCategoryNames) {
            const modules = categories[categoryName];
            const section = document.createElement('section');
            section.className = 'category-section';

            // Category Header
            const header = document.createElement('div');
            header.className = 'category-header';
            
            const title = document.createElement('h2');
            // Extract the first module to get the category index for numbering
            const index = modules.length > 0 ? modules[0].category_index : '';
            title.textContent = `${index}. ${categoryName}`;

            const stats = document.createElement('span');
            stats.className = 'category-stats';
            stats.id = `stats-${categoryName.replace(/[^a-zA-Z0-9]/g, '-')}`;
            
            header.appendChild(title);
            header.appendChild(stats);

            // Category Content
            const content = document.createElement('div');
            content.className = 'category-content';

            modules.forEach(module => {
                const card = document.createElement('div');
                card.className = 'module-card';

                const moduleState = state[module.id] || 'pending';

                card.innerHTML = `
                    <div class="module-header">
                        ${module.is_info ? '' : `
                        <div class="module-status" onclick="event.stopPropagation()">
                            <select class="status-select ${moduleState}" data-id="${module.id}">
                                <option value="pending" ${moduleState === 'pending' ? 'selected' : ''}>Pending</option>
                                <option value="done" ${moduleState === 'done' ? 'selected' : ''}>Done</option>
                                <option value="finding" ${moduleState === 'finding' ? 'selected' : ''}>Finding!</option>
                                <option value="na" ${moduleState === 'na' ? 'selected' : ''}>N/A</option>
                            </select>
                        </div>
                        `}
                        <div class="module-title-area">
                            ${module.is_info ? 
                                `<span>ℹ️ <strong>Information:</strong> ${module.title}</span>` :
                                `<span class="module-id">${module.id}</span>
                                 <span class="module-name">${module.title}</span>`
                            }
                        </div>
                        <div style="color: var(--text-secondary);">▼</div>
                    </div>
                    <div class="module-details">
                        ${module.is_info ? `
                        <div class="detail-section full-width">
                            <div class="detail-content">${marked.parse(module.full_text || 'No content available.')}</div>
                        </div>
                        ` : `
                        <div class="detail-section">
                            <h4>Relevance</h4>
                            <div class="detail-content">${module.relevance}</div>
                        </div>
                        <div class="detail-section">
                            <h4>Goal / Objectives</h4>
                            <div class="detail-content">${marked.parse(module.goal)}</div>
                        </div>
                        <div class="detail-section full-width docs-section" style="padding: 0;">
                            <div class="docs-header" style="padding: 1rem; display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none;">
                                <h4 style="margin: 0;">Documentation</h4>
                                <div class="docs-arrow" style="color: var(--text-secondary);">▼</div>
                            </div>
                            <div class="detail-content docs-content" style="display: none; padding: 0 1rem 1rem 1rem;">
                                    <h3 class="doc-section-title" style="margin-top: 0;">Summary</h3>
                                    ${marked.parse(module.full_summary || 'No summary specified.')}
                                    
                                    <h3 class="doc-section-title">Methodology</h3>
                                    ${marked.parse(module.methodology)}
                                    
                                    <h3 class="doc-section-title">Expected Evidence / Reporting</h3>
                                    <p><strong>Evidence:</strong> ${marked.parseInline ? marked.parseInline(module.expected_evidence) : module.expected_evidence}</p>
                                    <p><strong>Reporting:</strong> ${marked.parseInline ? marked.parseInline(module.reporting_hints) : marked.parse(module.reporting_hints).replace(/^<p>|<\/p>\n?$/g, '')}</p>
                                    
                                    <h3 class="doc-section-title">Tools</h3>
                                    ${marked.parse(module.tools || 'No specific tools mentioned.')}
                                    
                                    <div style="margin-top: 1.5rem; text-align: center;">
                                        <button class="docs-close-btn btn secondary">▲ Weniger anzeigen</button>
                                    </div>
                            </div>
                        </div>

                        <div class="detail-section full-width sysreptor-section" data-id="${module.id}">
                            <h4>SysReptor Integration</h4>
                            <div class="detail-content">
                                <div>
                                    <label style="font-size: 0.85rem; color: var(--text-secondary); display: block; margin-bottom: 4px;">Finding Title (Editable):</label>
                                    <input type="text" class="sysreptor-title-input" value="${(state[module.id + '_title'] || module.sysreptor_finding).replace(/"/g, '&quot;')}">
                                </div>
                                <div class="sysreptor-notes-container">
                                    <ul class="sysreptor-notes-list"></ul>
                                    <div class="sysreptor-images-list" style="margin-bottom: 10px; margin-top: 5px;"></div>
                                    <textarea class="sysreptor-note-textarea" placeholder="Hinweise hinzufügen (Bilder per Strg+V einfügen möglich)..."></textarea>
                                    <div style="display: flex; gap: 10px; margin-top: 5px;">
                                        <button class="sysreptor-add-note-btn">Hinweis hinzufügen</button>
                                        <button class="sysreptor-add-image-btn btn secondary" style="padding: 6px 12px; font-size: 0.85rem;">Bild(er) hinzufügen</button>
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
                        const arrow = modHeader.querySelector('div:last-child');
                        arrow.textContent = '▼';
                    } else {
                        modDetails.classList.add('open');
                        const arrow = modHeader.querySelector('div:last-child');
                        arrow.textContent = '▲';

                        // Scroll module into view smoothly
                        setTimeout(() => {
                            const rect = card.getBoundingClientRect();
                            let targetY;
                            if (rect.height > window.innerHeight - 100) {
                                // If the module is too large to fit the screen, scroll to its top with a little margin
                                targetY = rect.top + window.scrollY - 80;
                            } else {
                                // Otherwise, center it perfectly on the screen
                                targetY = rect.top + window.scrollY - (window.innerHeight / 2) + (rect.height / 2);
                            }
                            window.scrollTo({ top: targetY, behavior: 'smooth' });
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
                        let targetY = 0;
                        if (scrollToTop) {
                            // Calculate position BEFORE shrinking the card
                            targetY = card.getBoundingClientRect().top + window.scrollY - 120; // 120px offset for plenty of space
                        }
                        
                        docsContent.style.display = 'none';
                        docsArrow.textContent = '▼';
                        
                        if (scrollToTop) {
                            setTimeout(() => {
                                window.scrollTo({ top: targetY, behavior: 'smooth' });
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

                // Status Change
                if (!module.is_info) {
                    const select = card.querySelector('.status-select');
                    select.addEventListener('change', (e) => {
                        const newVal = e.target.value;
                        state[module.id] = newVal;
                        
                        // Update class
                        select.className = `status-select ${newVal}`;
                        
                        saveState();
                        updateProgress();
                    });

                    // SysReptor Logic
                    const titleInput = card.querySelector('.sysreptor-title-input');
                    const textarea = card.querySelector('.sysreptor-note-textarea');
                    const addBtn = card.querySelector('.sysreptor-add-note-btn');
                    const notesList = card.querySelector('.sysreptor-notes-list');

                    if (!titleInput) {
                        console.error("SysReptor fields missing for module:", module.id);
                        return; // skip event listeners for this card
                    }

                    titleInput.addEventListener('input', (e) => {
                        state[module.id + '_title'] = e.target.value;
                        saveState();
                    });

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
            header.addEventListener('click', () => {
                content.classList.toggle('open');
            });

            section.appendChild(header);
            section.appendChild(content);
            checklistContainer.appendChild(section);
        }
    };

    const updateProgress = () => {
        let completed = 0;
        let total = 0;

        // Also update category stats
        const categoryCounts = {};
        checklistData.forEach(module => {
            if (module.is_info) return;

            total++;
            if(!categoryCounts[module.category]) categoryCounts[module.category] = { total: 0, done: 0 };
            categoryCounts[module.category].total++;
            
            const moduleState = state[module.id];
            if (moduleState && moduleState !== 'pending') {
                completed++;
                categoryCounts[module.category].done++;
            }
        });

        progressText.textContent = `${completed} / ${total} Checked`;
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

    // Export/Import State
    exportBtn.addEventListener('click', async () => {
        const exportData = {};
        const zip = new JSZip();
        const imagesFolder = zip.folder("images");

        checklistData.forEach(module => {
            if (module.is_info) return;
            
            const status = state[module.id] || 'pending';
            const title = state[module.id + '_title'];
            const notes = state[module.id + '_notes'];
            const images = state[module.id + '_images'];
            
            if (status !== 'pending' || title || (notes && notes.length > 0) || (images && images.length > 0)) {
                exportData[module.id] = {
                    status: status,
                    title: title || module.sysreptor_finding
                };
                if (notes && notes.length > 0) {
                    exportData[module.id].notes = notes;
                }
                if (images && images.length > 0) {
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
                        const fileName = `${module.id}_${idx}.${ext}`;
                        exportData[module.id].images.push(fileName);
                        
                        const base64Data = imgData.split(',')[1];
                        imagesFolder.file(fileName, base64Data, {base64: true});
                    });
                }
            }
        });

        zip.file("wstg_pentest_state.json", JSON.stringify(exportData, null, 2));
        
        try {
            const content = await zip.generateAsync({type: "blob"});
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
            alert("Fehler beim Erstellen der ZIP-Datei.");
        }
    });

    importBtn.addEventListener('click', () => {
        importFile.click();
    });

    importFile.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

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
                alert("State imported successfully from ZIP!");
            } catch (err) {
                console.error(err);
                alert("Error importing ZIP file.");
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
                    alert("State imported successfully!");
                } catch (err) {
                    alert("Invalid JSON file.");
                }
            };
            reader.readAsText(file);
        }
        importFile.value = '';
    });

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            const confirmed = confirm("Warnung: Möchtest du wirklich deinen gesamten Fortschritt und alle Notizen unwiderruflich löschen?");
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
    loadData();
});
