from __future__ import annotations

import re
from io import BytesIO
from typing import Any, Dict, List

import pdfplumber

SECTION_RE = re.compile(r"\b(ingredients?|instructions?|method|directions?)\b", re.IGNORECASE)
PRICE_RE = re.compile(r"(\$|€|£)\s?\d+(?:\.\d{2})?")
TIME_RE = re.compile(r"(prep|cook|total)\s*time", re.IGNORECASE)


def extract_text(payload: bytes) -> str:
    with pdfplumber.open(BytesIO(payload)) as pdf:
        pages = []
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text)
    return "\n".join(pages)


def split_blocks(text: str) -> List[str]:
    return [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]


def parse_recipe_block(block: str) -> Dict[str, Any]:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if not lines:
        return {}

    title = lines[0]
    ingredients: List[str] = []
    instructions: List[str] = []
    mode = None

    for line in lines[1:]:
        if re.search(r"ingredients?", line, re.IGNORECASE):
            mode = "ingredients"
            continue
        if re.search(r"(instructions?|method|directions?)", line, re.IGNORECASE):
            mode = "instructions"
            continue

        if mode == "ingredients":
            ingredients.append(line)
        elif mode == "instructions":
            instructions.append(line)
        else:
            if not ingredients:
                ingredients.append(line)
            else:
                instructions.append(line)

    return {
        "title": title,
        "name": title,
        "ingredients": ingredients,
        "instructions": instructions,
        "source": "pdf",
    }


def parse_menu_block(block: str) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    lines = [line.strip() for line in block.splitlines() if line.strip()]

    for line in lines:
        price_match = PRICE_RE.search(line)
        if not price_match:
            continue
        price_value = price_match.group(0)
        name = line.replace(price_value, "").strip(" -–—.")
        items.append(
            {
                "name": name,
                "price": price_value,
                "description": "",
                "source": "pdf",
            }
        )
    return items


def classify_block(block: str) -> str:
    lines = block.lower()
    recipes_score = sum(m is not None for m in SECTION_RE.finditer(lines)) + sum(
        m is not None for m in TIME_RE.finditer(lines)
    )
    menu_score = len(PRICE_RE.findall(block)) * 2
    if menu_score > recipes_score:
        return "menu"
    if recipes_score:
        return "recipe"
    return "unknown"


def parse_pdf(payload: bytes, filename: str | None = None) -> Dict[str, Any]:
    text = extract_text(payload)
    if not text.strip():
        return {
            "recipes": [],
            "menu_items": [],
            "metadata": {"text_extracted": False},
            "warnings": ["No extractable text found in PDF."],
        }

    recipes: List[Dict[str, Any]] = []
    menu_items: List[Dict[str, Any]] = []

    for block in split_blocks(text):
        category = classify_block(block)
        if category == "recipe":
            parsed = parse_recipe_block(block)
            if parsed:
                recipes.append(parsed)
        elif category == "menu":
            menu_items.extend(parse_menu_block(block))

    metadata = {
        "filename": filename,
        "recipes_detected": len(recipes),
        "menu_items_detected": len(menu_items),
    }
    warnings: List[str] = []
    if not recipes and not menu_items:
        warnings.append("No recipes or menu items recognised. Manual review recommended.")

    return {
        "recipes": recipes,
        "menu_items": menu_items,
        "metadata": metadata,
        "warnings": warnings,
    }


