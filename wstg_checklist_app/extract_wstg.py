import os
import re
import json
from pathlib import Path

def parse_wstg_file(filepath, custom_relevance=None, custom_evidence=None, custom_tools=None):
    if custom_relevance is None:
        custom_relevance = {}
    if custom_evidence is None:
        custom_evidence = {}
    if custom_tools is None:
        custom_tools = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    if filename == "README.md":
        return None

    # Skip files that have been merged into other modules
    if "This content has been merged into:" in content:
        return None

    # Title is usually the first header
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filename.replace('.md', '')

    # Category is the parent directory
    category_raw = os.path.basename(os.path.dirname(filepath))
    category_index_match = re.search(r'^(\d+)-', category_raw)
    category_index = int(category_index_match.group(1)) if category_index_match else 99
    # clean up category name (e.g. 01-Information_Gathering -> Information Gathering)
    category = re.sub(r'^\d+-', '', category_raw).replace('_', ' ')

    is_info = False
    full_text = ""
    if filename.startswith('00-'):
        is_info = True
        wstg_id = f"INFO-{category.replace(' ', '-')}"
        full_text = re.sub(r'^#\s+.*?\n+', '', content, count=1).strip()
    else:
        # WSTG-ID
        id_match = re.search(r'\|(WSTG-[A-Z]+-\d+)\|', content)
        wstg_id = id_match.group(1) if id_match else "UNKNOWN-ID"

    # Extract sections using regex
    def extract_section(header):
        # Match header and everything until next header of same or higher level
        pattern = re.compile(rf'^##\s+{header}\s*\n(.*?)(?=\n##\s+|\Z)', re.MULTILINE | re.DOTALL | re.IGNORECASE)
        match = pattern.search(content)
        return match.group(1).strip() if match else ""
    
    def extract_subsection(header):
        # Match ## or ### for the header
        pattern = re.compile(rf'^#{{2,3}}\s+{header}\s*\n(.*?)(?=\n#{{2,3}}\s+|\Z)', re.MULTILINE | re.DOTALL | re.IGNORECASE)
        match = pattern.search(content)
        if not match:
            return ""
        
        extracted = match.group(1).strip()
        # Clean up CWE blocks which sometimes appear in Tools
        extracted = re.sub(r'```text\n(CWE-\d+.*?\n)+```', '', extracted, flags=re.MULTILINE)
        return extracted.strip()

    summary = extract_section("Summary")
    test_objectives = extract_section("Test Objectives")
    how_to_test = extract_section("How to Test")
    remediation = extract_section("Remediation")

    if wstg_id in custom_tools:
        tools_list = custom_tools[wstg_id]
        if tools_list:
            tools = "\n".join(f"- {t}" for t in tools_list)
        else:
            tools = "No specific tools mentioned."
    else:
        tools = extract_subsection("Tools")
        if not tools:
            pass
    
    # Short Relevance (first 1-2 sentences of summary) or custom relevance
    if wstg_id in custom_relevance:
        relevance = custom_relevance[wstg_id]
    else:
        relevance = "No description available."
        if summary:
            # Split by punctuation followed by space
            import re as regex
            sentences = regex.split(r'(?<=[.!?])\s+', summary.strip())
            # Clean up markdown chars for the short text
            clean_sentences = [s.replace('*', '').replace('`', '').replace('\n', ' ') for s in sentences]
            relevance = " ".join(clean_sentences[:2]) if clean_sentences else summary

    # Expected Evidence and Reporting Hints
    if wstg_id in custom_evidence:
        expected_evidence = custom_evidence[wstg_id].get("expected_evidence", "A working Proof of Concept (PoC) demonstrating the vulnerability. This should include the exact HTTP requests/responses, screenshots, or step-by-step instructions proving that the test objectives can be achieved.")
        reporting_hints = custom_evidence[wstg_id].get("reporting_hints", remediation if remediation else "Document the affected endpoint, the exact payload/parameters used, the business impact, and provide clear steps to reproduce.")
    else:
        expected_evidence = "A working Proof of Concept (PoC) demonstrating the vulnerability. This should include the exact HTTP requests/responses, screenshots, or step-by-step instructions proving that the test objectives can be achieved."
        reporting_hints = remediation if remediation else "Document the affected endpoint, the exact payload/parameters used, the business impact, and provide clear steps to reproduce."

    # Generic SysReptor Finding Title
    finding_title = f"{wstg_id}: {title}"

    return {
        "id": wstg_id,
        "is_info": is_info,
        "title": title,
        "category": category,
        "category_index": category_index,
        "goal": test_objectives if test_objectives else "No goal defined.",
        "relevance": relevance,
        "full_summary": summary if summary else "No summary provided.",
        "full_text": full_text,
        "methodology": how_to_test if how_to_test else "No methodology defined.",
        "tools": tools,
        "expected_evidence": expected_evidence,
        "reporting_hints": reporting_hints,
        "sysreptor_finding": finding_title
    }

def main():
    base_dir = Path("/home/len/Festplatte/wstg/document/4-Web_Application_Security_Testing")
    checklist = []

    if not base_dir.exists():
        print(f"Error: {base_dir} does not exist.")
        return

    # Load custom relevance file if it exists
    custom_relevance = {}
    relevance_file = Path("/home/len/Festplatte/wstg/wstg_checklist_app/wstg_relevance.json")
    if relevance_file.exists():
        try:
            with open(relevance_file, 'r', encoding='utf-8') as f:
                custom_relevance = json.load(f)
            print(f"Loaded {len(custom_relevance)} custom relevance summaries.")
        except Exception as e:
            print(f"Failed to load custom relevance file: {e}")

    # Load custom evidence and reporting file if it exists
    custom_evidence = {}
    evidence_file = Path("/home/len/Festplatte/wstg/wstg_checklist_app/wstg_evidence_reporting.json")
    if evidence_file.exists():
        try:
            with open(evidence_file, 'r', encoding='utf-8') as f:
                evidence_list = json.load(f)
                for item in evidence_list:
                    if "id" in item:
                        custom_evidence[item["id"]] = item
            print(f"Loaded {len(custom_evidence)} custom evidence/reporting hints.")
        except Exception as e:
            print(f"Failed to load custom evidence file: {e}")

    # Load custom tools file if it exists
    custom_tools = {}
    tools_file = Path("/home/len/Festplatte/wstg/wstg_checklist_app/wstg_tools.json")
    if tools_file.exists():
        try:
            with open(tools_file, 'r', encoding='utf-8') as f:
                tools_list = json.load(f)
                for item in tools_list:
                    if "id" in item:
                        custom_tools[item["id"]] = item.get("tools", [])
            print(f"Loaded {len(custom_tools)} custom tools lists.")
        except Exception as e:
            print(f"Failed to load custom tools file: {e}")

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                module_data = parse_wstg_file(filepath, custom_relevance, custom_evidence, custom_tools)
                if module_data and module_data['id'] != "UNKNOWN-ID":
                    checklist.append(module_data)

    # Sort by ID
    checklist.sort(key=lambda x: x['id'])

    output_path = "/home/len/Festplatte/wstg/wstg_checklist_app/wstg_checklist_data.js"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("const wstgData = ")
        json.dump(checklist, f, indent=4)
        f.write(";\n")
    
    print(f"Parsed {len(checklist)} modules successfully. Saved to {output_path}")

if __name__ == "__main__":
    main()
