#!/usr/bin/env python3
"""Render KeepRight spec derivatives from spec.json."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any
from xml.dom import minidom
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "spec.json"
OUTPUT_ROOT = ROOT / "i18n"

COUNTRIES = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Brunei",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cabo Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Comoros",
    "Congo",
    "Costa Rica",
    "Croatia",
    "Cuba",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini",
    "Ethiopia",
    "Fiji",
    "Finland",
    "France",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Kuwait",
    "Kyrgyzstan",
    "Laos",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Micronesia",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "North Korea",
    "North Macedonia",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Russia",
    "Rwanda",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Korea",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Syria",
    "Taiwan",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Vatican City",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]


def load_spec() -> dict[str, Any]:
    with SPEC_PATH.open("r", encoding="utf-8") as source:
        return json.load(source)


def local_text(value: Any, locale: str) -> str:
    if isinstance(value, dict):
        return str(value.get(locale) or value.get("en-GB") or next(iter(value.values()), ""))
    if value is None:
        return ""
    return str(value)


def title_for(item: dict[str, Any], locale: str) -> str:
    return local_text(item.get("title"), locale)


def label_for(item: dict[str, Any], locale: str) -> str:
    label = local_text(item.get("label"), locale)
    optional = local_text(item.get("optionalLabel"), locale)
    if optional:
        label = f"{label} ({optional})"
    code = item.get("displayCode")
    return f"{code}. {label}" if code else label


def description_for(item: dict[str, Any], locale: str) -> str:
    return local_text(item.get("description"), locale)


def condition_to_text(condition: dict[str, Any] | None) -> str:
    if not condition:
        return ""
    if "ref" in condition:
        return f"condition `{condition['ref']}`"
    if "field" in condition and "equals" in condition:
        return f"`{condition['field']}` equals `{condition['equals']}`"
    if "field" in condition and "contains" in condition:
        return f"`{condition['field']}` contains `{condition['contains']}`"
    if "any" in condition:
        return "any of " + "; ".join(condition_to_text(part) for part in condition["any"])
    if "all" in condition:
        return "all of " + "; ".join(condition_to_text(part) for part in condition["all"])
    return json.dumps(condition, ensure_ascii=False, sort_keys=True)


def source_options(spec: dict[str, Any], source_name: str, locale: str) -> list[dict[str, Any]]:
    if source_name == "countries":
        return [{"value": country, "label": {locale: country}} for country in COUNTRIES]
    raise ValueError(f"Unsupported option source: {source_name}")


def question_options(
    spec: dict[str, Any],
    item: dict[str, Any],
    locale: str,
    expand_sources: bool = True,
) -> list[dict[str, Any]]:
    if "options" in item:
        return item["options"]
    if expand_sources and "optionSource" in item:
        return source_options(spec, item["optionSource"], locale)
    return []


def option_source_description(spec: dict[str, Any], source_name: str, locale: str) -> str:
    source = spec["meta"].get("optionSources", {}).get(source_name, {})
    parts = [source_name]
    if source.get("source"):
        parts.append(str(source["source"]))
    return "; ".join(parts)


def select_empty_option_label() -> str:
    return "Select an option"


def iter_child_items(item: dict[str, Any]) -> list[dict[str, Any]]:
    return item.get("items", [])


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def metadata_line(spec: dict[str, Any]) -> str:
    meta = spec["meta"]
    return (
        f"Release: {meta.get('release', '')}; "
        f"Spec version: {meta.get('specVersion', '')}; "
        f"Schema version: {meta.get('schemaVersion', '')}"
    )


def render_txt(spec: dict[str, Any], locale: str) -> str:
    lines: list[str] = []
    title = local_text(spec["meta"].get("title"), locale)
    if title:
        lines.extend([title, "=" * len(title), metadata_line(spec), ""])

    def add_question(item: dict[str, Any], indent: int) -> None:
        pad = " " * indent
        lines.append(f"{pad}{label_for(item, locale)}")
        lines.append(f"{pad}Answer type: {item.get('answerType')}")
        if "visibleWhen" in item:
            lines.append(f"{pad}Shown when: {condition_to_text(item['visibleWhen'])}")
        if "optionSource" in item:
            lines.append(f"{pad}Option source: {option_source_description(spec, item['optionSource'], locale)}")
        options = question_options(spec, item, locale, expand_sources=False)
        if options:
            lines.append(f"{pad}Options:")
            for option in options:
                lines.append(f"{pad}- {local_text(option.get('label'), locale)} [{option.get('value')}]")
        if item.get("followups"):
            lines.append(f"{pad}Follow-ups:")
            for followup in item["followups"]:
                details = f"{label_for(followup, locale)} [{followup.get('answerType')}]"
                if "visibleWhen" in followup:
                    details += f"; shown when {condition_to_text(followup['visibleWhen'])}"
                lines.append(f"{pad}- {details}")
        lines.append("")

    def walk(items: list[dict[str, Any]], indent: int = 0) -> None:
        for item in items:
            kind = item.get("kind")
            pad = " " * indent
            if kind == "group":
                group_title = title_for(item, locale)
                if group_title:
                    lines.extend([f"{pad}{group_title}", f"{pad}{'-' * len(group_title)}"])
                if "visibleWhen" in item:
                    lines.append(f"{pad}Shown when: {condition_to_text(item['visibleWhen'])}")
                if group_title or "visibleWhen" in item:
                    lines.append("")
                walk(iter_child_items(item), indent + 2)
            elif kind == "question":
                add_question(item, indent)
            elif kind == "note":
                lines.extend([f"{pad}{local_text(item.get('text'), locale)}", ""])

    for section in spec["sections"]:
        heading = title_for(section, locale)
        lines.extend([heading, "-" * len(heading)])
        description = description_for(section, locale)
        if description:
            lines.extend([description, ""])
        walk(iter_child_items(section), 0)
    return "\n".join(lines)


def render_md(spec: dict[str, Any], locale: str) -> str:
    lines: list[str] = []
    title = local_text(spec["meta"].get("title"), locale)
    if title:
        lines.extend([f"# {title}", "", metadata_line(spec), ""])

    def add_question(item: dict[str, Any]) -> None:
        lines.append(f"**{label_for(item, locale)}**")
        lines.append("")
        lines.append(f"- Answer type: `{item.get('answerType')}`")
        if "visibleWhen" in item:
            lines.append(f"- Shown when: {condition_to_text(item['visibleWhen'])}")
        if "optionSource" in item:
            lines.append(f"- Option source: {option_source_description(spec, item['optionSource'], locale)}")
        options = question_options(spec, item, locale, expand_sources=False)
        if options:
            lines.append("- Options:")
            for option in options:
                lines.append(f"  - `{option.get('value')}`: {local_text(option.get('label'), locale)}")
        if item.get("followups"):
            lines.append("- Follow-ups:")
            for followup in item["followups"]:
                detail = f"{label_for(followup, locale)} (`{followup.get('answerType')}`)"
                if "visibleWhen" in followup:
                    detail += f", shown when {condition_to_text(followup['visibleWhen'])}"
                lines.append(f"  - {detail}")
        lines.append("")

    def walk(items: list[dict[str, Any]], depth: int) -> None:
        for item in items:
            kind = item.get("kind")
            if kind == "group":
                group_title = title_for(item, locale)
                if group_title:
                    lines.extend([f"{'#' * depth} {group_title}", ""])
                if "visibleWhen" in item:
                    lines.extend([f"_Shown when: {condition_to_text(item['visibleWhen'])}_", ""])
                walk(iter_child_items(item), min(depth + 1, 6))
            elif kind == "question":
                add_question(item)
            elif kind == "note":
                lines.extend([local_text(item.get("text"), locale), ""])

    for section in spec["sections"]:
        lines.extend([f"## {title_for(section, locale)}", ""])
        description = description_for(section, locale)
        if description:
            lines.extend([description, ""])
        walk(iter_child_items(section), 3)
    return "\n".join(lines)


def render_static_html(spec: dict[str, Any], locale: str) -> str:
    title = local_text(spec["meta"].get("title"), locale)
    body: list[str] = [
        f"<h1>{html.escape(title)}</h1>",
        f"<p>{html.escape(metadata_line(spec))}</p>",
    ]
    for section in spec["sections"]:
        body.append("<section>")
        body.append(f"<h2>{html.escape(title_for(section, locale))}</h2>")
        description = description_for(section, locale)
        if description:
            body.append(f"<p>{html.escape(description)}</p>")
        for item in iter_child_items(section):
            body.append(render_static_item(spec, item, locale, 3))
        body.append("</section>")
    return html_document(title, locale, "\n".join(body), presentation_css())


def render_static_item(spec: dict[str, Any], item: dict[str, Any], locale: str, heading_level: int) -> str:
    kind = item.get("kind")
    if kind == "group":
        parts = ['<section class="spec-group">']
        title = title_for(item, locale)
        if title:
            parts.append(f"<h{heading_level}>{html.escape(title)}</h{heading_level}>")
        if "visibleWhen" in item:
            parts.append(f"<p><em>Shown when: {html.escape(condition_to_text(item['visibleWhen']))}</em></p>")
        for child in iter_child_items(item):
            parts.append(render_static_item(spec, child, locale, min(heading_level + 1, 6)))
        parts.append("</section>")
        return "\n".join(parts)
    if kind == "note":
        return f"<p>{html.escape(local_text(item.get('text'), locale))}</p>"
    if kind == "question":
        parts = ['<section class="spec-question">', f"<h{heading_level}>{html.escape(label_for(item, locale))}</h{heading_level}>", "<ul>"]
        parts.append(f"<li>Answer type: <code>{html.escape(str(item.get('answerType')))}</code></li>")
        if "visibleWhen" in item:
            parts.append(f"<li>Shown when: {html.escape(condition_to_text(item['visibleWhen']))}</li>")
        if "optionSource" in item:
            parts.append(f"<li>Option source: {html.escape(option_source_description(spec, item['optionSource'], locale))}</li>")
        options = question_options(spec, item, locale, expand_sources=False)
        if options:
            parts.append("<li>Options:<ul>")
            for option in options:
                parts.append(f"<li><code>{html.escape(str(option.get('value')))}</code>: {html.escape(local_text(option.get('label'), locale))}</li>")
            parts.append("</ul></li>")
        if item.get("followups"):
            parts.append("<li>Follow-ups:<ul>")
            for followup in item["followups"]:
                detail = f"{label_for(followup, locale)} ({followup.get('answerType')})"
                if "visibleWhen" in followup:
                    detail += f"; shown when {condition_to_text(followup['visibleWhen'])}"
                parts.append(f"<li>{html.escape(detail)}</li>")
            parts.append("</ul></li>")
        parts.extend(["</ul>", "</section>"])
        return "\n".join(parts)
    return ""


def html_document(title: str, locale: str, body: str, css: str, script: str = "") -> str:
    script_tag = f"\n<script>\n{script}\n</script>" if script else ""
    return f"""<!doctype html>
<html lang="{html.escape(locale)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
{css}
  </style>
</head>
<body>
  <main>
{body}
  </main>{script_tag}
</body>
</html>"""


def presentation_css() -> str:
    return """    :root { color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.5; }
    body { margin: 0; padding: 2rem; background: Canvas; color: CanvasText; }
    main { max-width: 48rem; margin: 0 auto; }
    h1, h2, h3 { line-height: 1.15; margin: 2rem 0 0.75rem; }
    h1:first-child { margin-top: 0; }
    p, ul { margin: 0.75rem 0; }
    li { margin: 0.25rem 0; }
    code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.94em; }"""


def render_xml(spec: dict[str, Any], locale: str) -> str:
    root = ET.Element(
        "keepRightSpec",
        {
            "schemaVersion": spec["meta"].get("schemaVersion", ""),
            "specVersion": spec["meta"].get("specVersion", ""),
            "release": spec["meta"].get("release", ""),
            "locale": locale,
        },
    )
    ET.SubElement(root, "title").text = local_text(spec["meta"].get("title"), locale)
    render_logic_xml(root, spec.get("logic", {}))
    sections = ET.SubElement(root, "sections")
    for section in spec["sections"]:
        render_item_xml(sections, section, spec, locale, tag="section")
    rough = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")


def render_logic_xml(parent: ET.Element, logic: dict[str, Any]) -> None:
    logic_el = ET.SubElement(parent, "logic")
    conditions_el = ET.SubElement(logic_el, "conditions")
    for name, condition in logic.get("conditions", {}).items():
        condition_el = ET.SubElement(conditions_el, "condition", {"id": name})
        append_condition_xml(condition_el, condition)


def append_condition_xml(parent: ET.Element, condition: dict[str, Any]) -> None:
    if "ref" in condition:
        ET.SubElement(parent, "ref").text = str(condition["ref"])
    if "field" in condition:
        attrs = {"field": str(condition["field"])}
        if "equals" in condition:
            attrs["equals"] = str(condition["equals"])
        if "contains" in condition:
            attrs["contains"] = str(condition["contains"])
        ET.SubElement(parent, "fieldCondition", attrs)
    for operator in ("any", "all"):
        if operator in condition:
            op_el = ET.SubElement(parent, operator)
            for part in condition[operator]:
                part_el = ET.SubElement(op_el, "condition")
                append_condition_xml(part_el, part)


def render_item_xml(
    parent: ET.Element,
    item: dict[str, Any],
    spec: dict[str, Any],
    locale: str,
    tag: str = "item",
) -> None:
    attrs = {"id": item["id"]}
    if "kind" in item:
        attrs["kind"] = item["kind"]
    if "answerType" in item:
        attrs["answerType"] = item["answerType"]
    if "displayCode" in item:
        attrs["displayCode"] = item["displayCode"]
    if "optionSource" in item:
        attrs["optionSource"] = item["optionSource"]
    element = ET.SubElement(parent, tag, attrs)
    for key in ("title", "label", "description", "text", "optionalLabel"):
        if key in item:
            ET.SubElement(element, key).text = local_text(item[key], locale)
    if "visibleWhen" in item:
        visible = ET.SubElement(element, "visibleWhen")
        append_condition_xml(visible, item["visibleWhen"])
    if "labelVariants" in item:
        variants = ET.SubElement(element, "labelVariants")
        for variant in item["labelVariants"]:
            variant_el = ET.SubElement(variants, "variant")
            when = ET.SubElement(variant_el, "when")
            append_condition_xml(when, variant["when"])
            ET.SubElement(variant_el, "label").text = local_text(variant["label"], locale)
    if "ui" in item:
        ui = ET.SubElement(element, "ui")
        for key, value in item["ui"].items():
            ET.SubElement(ui, key).text = str(value)
    options = question_options(spec, item, locale)
    if options:
        options_el = ET.SubElement(element, "options")
        for option in options:
            option_el = ET.SubElement(options_el, "option", {"value": str(option["value"])})
            ET.SubElement(option_el, "label").text = local_text(option.get("label"), locale)
    if "followups" in item:
        followups = ET.SubElement(element, "followups")
        for followup in item["followups"]:
            render_item_xml(followups, followup, spec, locale)
    if "items" in item:
        items = ET.SubElement(element, "items")
        for child in item["items"]:
            render_item_xml(items, child, spec, locale)
    if "result" in item:
        result = ET.SubElement(element, "result")
        for key, value in item["result"].items():
            ET.SubElement(result, key).text = str(value)


def render_form_html(spec: dict[str, Any], locale: str) -> str:
    title = local_text(spec["meta"].get("title"), locale)
    content: list[str] = [
        f'<h1>{html.escape(title)}</h1>',
        f"<p>{html.escape(metadata_line(spec))}</p>",
        '<form id="keepright-form">',
    ]
    for section in spec["sections"]:
        content.append(render_form_section(spec, section, locale))
    content.append("</form>")
    body = "\n".join(f"    {line}" for line in content)
    config = {
        "conditions": spec.get("logic", {}).get("conditions", {}),
    }
    script = f"const specConfig = {json.dumps(config, ensure_ascii=False, sort_keys=True)};\n{form_script()}"
    return html_document(title, locale, body, form_css(), script)


def render_form_section(spec: dict[str, Any], section: dict[str, Any], locale: str) -> str:
    attrs = form_attrs(section)
    parts = [f'<section{attrs}>', f"  <h2>{html.escape(title_for(section, locale))}</h2>"]
    description = description_for(section, locale)
    if description:
        parts.append(f"  <p>{html.escape(description)}</p>")
    for item in iter_child_items(section):
        parts.append(render_form_item(spec, item, locale))
    parts.append("</section>")
    return "\n".join(parts)


def render_form_item(spec: dict[str, Any], item: dict[str, Any], locale: str) -> str:
    kind = item.get("kind")
    attrs = form_attrs(item)
    if kind == "group":
        parts = [f'<fieldset{attrs}>']
        title = title_for(item, locale)
        if title:
            parts.append(f"  <legend>{html.escape(title)}</legend>")
        for child in iter_child_items(item):
            parts.append(indent(render_form_item(spec, child, locale), 2))
        parts.append("</fieldset>")
        return "\n".join(parts)
    if kind == "note":
        return f'<p{attrs}>{html.escape(local_text(item.get("text"), locale))}</p>'
    if kind == "question":
        return render_form_question(spec, item, locale, attrs)
    return ""


def render_form_question(spec: dict[str, Any], item: dict[str, Any], locale: str, attrs: str) -> str:
    answer_type = item.get("answerType")
    question_id = item["id"]
    label_id = f"{question_id}-label"
    parts = [f'<div{attrs}>', f'  <label id="{label_id}" class="question-label" for="{question_id}">{html.escape(label_for(item, locale))}</label>']
    if answer_type in {"text", "email"}:
        parts.append(f'  <input type="{answer_type}" id="{question_id}" name="{question_id}">')
    elif answer_type == "textarea":
        rows = int(item.get("ui", {}).get("rows", 3))
        parts.append(f'  <textarea id="{question_id}" name="{question_id}" rows="{rows}"></textarea>')
    elif answer_type == "select":
        parts.append(f'  <select id="{question_id}" name="{question_id}">')
        empty_option_label = select_empty_option_label()
        parts.append(f'    <option value="">{html.escape(empty_option_label)}</option>')
        for option in question_options(spec, item, locale):
            value = html.escape(str(option["value"]))
            parts.append(f'    <option value="{value}">{html.escape(local_text(option.get("label"), locale))}</option>')
        parts.append("  </select>")
    elif answer_type in {"radio", "checkboxes"}:
        input_type = "checkbox" if answer_type == "checkboxes" else "radio"
        parts.append(f'  <div class="options" role="group" aria-labelledby="{label_id}">')
        for option in question_options(spec, item, locale):
            value = str(option["value"])
            input_id = f"{question_id}-{value}"
            parts.append("    <label>")
            parts.append(f'      <input type="{input_type}" id="{html.escape(input_id)}" name="{question_id}" value="{html.escape(value)}">')
            parts.append(f'      {html.escape(local_text(option.get("label"), locale))}')
            parts.append("    </label>")
        parts.append("  </div>")
    else:
        parts.append(f"  <p>Unsupported answer type: {html.escape(str(answer_type))}</p>")
    for followup in item.get("followups", []):
        followup_attrs = form_attrs(followup, classes="followup")
        parts.append(indent(render_form_question(spec, followup, locale, followup_attrs), 2))
    parts.append("</div>")
    return "\n".join(parts)


def form_attrs(item: dict[str, Any], classes: str = "field") -> str:
    attrs = [f'class="{classes}"', f'data-spec-id="{html.escape(item["id"])}"']
    if "displayCode" in item:
        attrs.append(f'data-display-code="{html.escape(item["displayCode"])}"')
    if "visibleWhen" in item:
        attrs.append(f"data-visible-when='{html.escape(json.dumps(item['visibleWhen'], ensure_ascii=False, sort_keys=True), quote=True)}'")
    if "labelVariants" in item:
        attrs.append(f"data-label-variants='{html.escape(json.dumps(item['labelVariants'], ensure_ascii=False, sort_keys=True), quote=True)}'")
    return " " + " ".join(attrs)

def indent(text: str, spaces: int) -> str:
    prefix = " " * spaces
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def form_css() -> str:
    return """    :root { color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.5; }
    body { margin: 0; padding: 2rem; background: Canvas; color: CanvasText; }
    main { max-width: 48rem; margin: 0 auto; }
    h1, h2 { line-height: 1.15; }
    section { border-top: 1px solid color-mix(in srgb, CanvasText 25%, transparent); padding: 1.5rem 0; }
    fieldset { border: 1px solid color-mix(in srgb, CanvasText 25%, transparent); border-radius: 0.6rem; margin: 1rem 0; padding: 1rem; }
    legend, .question-label { font-weight: 700; }
    .field { margin: 1rem 0; }
    .followup { margin: 0.75rem 0 0.75rem 1.5rem; }
    input[type='text'], input[type='email'], textarea, select { box-sizing: border-box; display: block; margin-top: 0.35rem; max-width: 100%; width: 32rem; }
    textarea { width: 40rem; }
    .options { margin-top: 0.35rem; }
    .options label { display: block; margin: 0.25rem 0; font-weight: 400; }
    [hidden] { display: none !important; }
    button { font: inherit; padding: 0.55rem 0.9rem; }"""


def form_script() -> str:
    return r"""const form = document.getElementById("keepright-form");

function fieldValues(fieldName) {
  const controls = Array.from(form.elements).filter((control) => control.name === fieldName);
  if (!controls.length) return [];
  const first = controls[0];
  if (first.type === "radio") {
    const checked = controls.find((control) => control.checked);
    return checked ? [checked.value] : [];
  }
  if (first.type === "checkbox") {
    return controls.filter((control) => control.checked).map((control) => control.value);
  }
  return first.value ? [first.value] : [];
}

function evaluateCondition(condition) {
  if (!condition) return true;
  if (condition.ref) return evaluateCondition(specConfig.conditions[condition.ref]);
  if (condition.any) return condition.any.some(evaluateCondition);
  if (condition.all) return condition.all.every(evaluateCondition);
  const values = fieldValues(condition.field);
  if (Object.prototype.hasOwnProperty.call(condition, "equals")) {
    return values.includes(condition.equals);
  }
  if (Object.prototype.hasOwnProperty.call(condition, "contains")) {
    return values.includes(condition.contains);
  }
  return true;
}

function clearControls(container) {
  container.querySelectorAll("input, textarea, select").forEach((control) => {
    if (control.type === "radio" || control.type === "checkbox") {
      control.checked = false;
    } else {
      control.value = "";
    }
  });
}

function applyVisibility() {
  document.querySelectorAll("[data-visible-when]").forEach((element) => {
    const condition = JSON.parse(element.dataset.visibleWhen);
    const visible = evaluateCondition(condition);
    if (element.hidden && visible) {
      element.hidden = false;
    } else if (!element.hidden && !visible) {
      clearControls(element);
      element.hidden = true;
    }
  });
}

function localized(value) {
  return value && (value["en-GB"] || Object.values(value)[0] || "");
}

function applyLabelVariants() {
  document.querySelectorAll("[data-label-variants]").forEach((element) => {
    const variants = JSON.parse(element.dataset.labelVariants);
    const label = element.querySelector(".question-label");
    if (!label) return;
    if (!label.dataset.defaultText) label.dataset.defaultText = label.textContent;
    const match = variants.find((variant) => evaluateCondition(variant.when));
    if (match) {
      const code = element.dataset.displayCode;
      const variantLabel = localized(match.label);
      label.textContent = code ? `${code}. ${variantLabel}` : variantLabel;
    } else {
      label.textContent = label.dataset.defaultText;
    }
  });
}

function updateForm() {
  applyVisibility();
  applyLabelVariants();
}

form.addEventListener("input", updateForm);
form.addEventListener("change", updateForm);

updateForm();"""


def main() -> None:
    spec = load_spec()
    locale = spec["meta"].get("defaultLocale", "en-GB")
    output_dir = OUTPUT_ROOT / locale
    write(output_dir / "spec.txt", render_txt(spec, locale))
    write(output_dir / "spec.md", render_md(spec, locale))
    write(output_dir / "spec.html", render_static_html(spec, locale))
    write(output_dir / "spec.xml", render_xml(spec, locale))
    write(output_dir / "spec_form.html", render_form_html(spec, locale))


if __name__ == "__main__":
    main()
