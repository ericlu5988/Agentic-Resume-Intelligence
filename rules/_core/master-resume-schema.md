# Master Resume Schema (v1.2) - Agentic Reference Guideline

This document serves as the **Source of Truth** for the Agent when mapping data from source documents (PDF/DOCX) into JSON and when generating **Bespoke Templates**. It ensures consistency across built-in templates while providing a deterministic structure for custom layouts.

## 1. Governance Principles
- **Guideline Status**: This schema is a *guideline* for the Agent. It defines the "Golden Path" for data structure.
- **Bespoke Trigger**: When a user requests a "Bespoke" or "Custom" template, the Agent **MUST** use this schema as the blueprint for both the JSON data and the LaTeX variable names.
- **Zero-Drop Policy**: No data from the source document should be discarded. If a section does not fit a "Core" key, it **MUST** be placed in `custom_sections`.

## 2. Core Schema Specification

### Contact & Metadata (`resume.*`)
| Key | Type | Description |
| :--- | :--- | :--- |
| `name` | String | Full name. |
| `phone` | String | Primary phone number. |
| `cell_phone` | String | Optional secondary/cell phone. |
| `email` | String | Primary email address. |
| `location` | String | City, State (or full address). |
| `linkedin` | String | LinkedIn URL/profile handle. |
| `clearance` | String | Security clearance level (e.g., TS/SCI). |
| `citizenship` | String | Citizenship status (Federal requirement). |
| `veterans_preference` | String | Veteran status (Federal requirement). |
| `federal_employment_status` | String | Current federal status. |
| `target_job_title` | String | The role being targeted. |
| `summary` | String | Professional summary or executive summary. |

### Experience (`resume.experience[]`)
| Key | Type | Description |
| :--- | :--- | :--- |
| `company` | String | Name of the organization. |
| `location` | String | City, State of the office. |
| `title` | String | Job title/Role. |
| `start_date` | String | e.g., "Jan 2022". |
| `end_date` | String | e.g., "Present" or "Dec 2023". |
| `details` | String | Optional high-level summary of the role. |
| `highlight_label` | String | Optional label for a "Key Impact" section. |
| `bullets` | Array | List of accomplishment/duty strings. |
| `supervisor` | String | Supervisor name (Federal). |
| `supervisor_phone` | String | Supervisor contact (Federal). |
| `hours_per_week` | String | Work hours (Federal). |
| `salary` | String | Compensation (Federal). |

### Education (`resume.education[]`)
| Key | Type | Description |
| :--- | :--- | :--- |
| `school` | String | Institution name. |
| `location` | String | City, State. |
| `degree` | String | Degree earned (e.g., B.S. Cybersecurity). |
| `date` | String | Graduation date. |
| `gpa` | String | Numerical GPA. |
| `focus` | String | Specialization or Minor. |

### Skills & Certifications
| Key | Type | Description |
| :--- | :--- | :--- |
| `skills` | Array | Flat list of general/soft skills. |
| `technical_skills` | Object | Dict of "Category Name": ["Skill1", "Skill2"]. |
| `certifications` | Array | List of professional certifications. |
| `awards` | Array | List of honors and awards. |
| `training` | Array | List of job-related training. |

## 3. The Extensibility Protocol (Catch-All)
If the source resume contains a section header that is **not** covered by the keys above (e.g., "Patents", "Volunteer Work", "Publications"), the Agent **MUST** map it to the `custom_sections` array.

```json
"custom_sections": [
  {
    "title": "Volunteer Work",
    "content": "A paragraph describing general volunteer activities.",
    "list_items": [
      "Built houses with Habitat for Humanity.",
      "Mentored youth in STEM programs."
    ]
  }
]
```

## 4. Bespoke Template Syntax
When the Agent generates a bespoke LaTeX template, it should use the following Jinja2 syntax to remain compatible with `importer_engine.py`:

- **Variable Access**: `((( resume.key|latex_escape )))`
- **Loops**: `((% for item in resume.experience %)) ... ((% endfor %))`
- **Conditionals**: `((% if resume.clearance %)) ... ((% endif %))`
