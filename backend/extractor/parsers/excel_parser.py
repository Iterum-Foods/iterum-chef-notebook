from __future__ import annotations

import io
from typing import Any, Dict, List, Tuple

import pandas as pd

RECIPE_NAME_CANDIDATES = {"recipe", "recipe_name", "name", "title", "dish"}
INGREDIENT_COLUMNS = {"ingredients", "ingredient_list", "components"}
INSTRUCTION_COLUMNS = {"instructions", "method", "directions"}
MENU_NAME_COLUMNS = {"item", "item_name", "dish", "menu_item"}
PRICE_COLUMNS = {"price", "cost", "amount"}


def load_workbook(payload: bytes, extension: str) -> List[Tuple[str, pd.DataFrame]]:
    buffer = io.BytesIO(payload)
    if extension == ".csv":
        df = pd.read_csv(buffer)
        return [("Sheet1", df)]

    dataframes: List[Tuple[str, pd.DataFrame]] = []
    with pd.ExcelFile(buffer) as workbook:
        for sheet_name in workbook.sheet_names:
            df = workbook.parse(sheet_name)
            dataframes.append((sheet_name, df))
    return dataframes


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    return df


def detect_recipe_sheet(df: pd.DataFrame) -> bool:
    cols = set(df.columns)
    has_name = bool(RECIPE_NAME_CANDIDATES & cols)
    has_ingredients = bool(INGREDIENT_COLUMNS & cols)
    return has_name and has_ingredients


def detect_menu_sheet(df: pd.DataFrame) -> bool:
    cols = set(df.columns)
    has_name = bool(MENU_NAME_COLUMNS & cols)
    has_price = bool(PRICE_COLUMNS & cols)
    return has_name and has_price


def rows_to_recipes(df: pd.DataFrame) -> List[Dict[str, Any]]:
    recipes: List[Dict[str, Any]] = []
    for _, row in df.iterrows():
        name = next((row.get(col) for col in RECIPE_NAME_CANDIDATES if col in row), None)
        if not name or not str(name).strip():
            continue

        ingredients = []
        for col in INGREDIENT_COLUMNS:
            if col in row and pd.notna(row[col]):
                ingredients = [part.strip() for part in str(row[col]).split("\n") if part.strip()]
                break

        instructions = []
        for col in INSTRUCTION_COLUMNS:
            if col in row and pd.notna(row[col]):
                instructions = [part.strip() for part in str(row[col]).split("\n") if part.strip()]
                break

        recipes.append(
            {
                "name": str(name).strip(),
                "title": str(name).strip(),
                "description": str(row.get("description", "")).strip(),
                "ingredients": ingredients,
                "instructions": instructions,
                "servings": row.get("servings") if pd.notna(row.get("servings")) else None,
                "tags": [
                    str(row[col]).strip()
                    for col in ["category", "cuisine", "tags"]
                    if col in row and pd.notna(row[col])
                ],
                "source": "excel",
            }
        )
    return recipes


def rows_to_menu_items(df: pd.DataFrame) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for _, row in df.iterrows():
        name = next((row.get(col) for col in MENU_NAME_COLUMNS if col in row), None)
        if not name or not str(name).strip():
            continue
        price = next((row.get(col) for col in PRICE_COLUMNS if col in row), None)

        items.append(
            {
                "name": str(name).strip(),
                "price": float(price) if price not in (None, "") and pd.notna(price) else None,
                "description": str(row.get("description", "")).strip(),
                "category": str(row.get("category", "")).strip(),
                "source": "excel",
            }
        )
    return items


def parse_excel(payload: bytes, filename: str | None, extension: str) -> Dict[str, Any]:
    dataframes = load_workbook(payload, extension)

    all_recipes: List[Dict[str, Any]] = []
    all_menu_items: List[Dict[str, Any]] = []
    warnings: List[str] = []

    for sheet_name, raw_df in dataframes:
        if raw_df.empty:
            continue

        df = normalize_columns(raw_df)
        df = df.dropna(how="all")
        if df.empty:
            continue

        if detect_recipe_sheet(df):
            recipes = rows_to_recipes(df)
            if recipes:
                for recipe in recipes:
                    recipe["sheet"] = sheet_name
                all_recipes.extend(recipes)
            else:
                warnings.append(f"No recipes detected in sheet '{sheet_name}'.")
        elif detect_menu_sheet(df):
            menu_items = rows_to_menu_items(df)
            if menu_items:
                for item in menu_items:
                    item["sheet"] = sheet_name
                all_menu_items.extend(menu_items)
            else:
                warnings.append(f"No menu items detected in sheet '{sheet_name}'.")
        else:
            warnings.append(f"Sheet '{sheet_name}' did not match recipe or menu patterns.")

    metadata = {
        "filename": filename,
        "sheets_processed": len(dataframes),
        "recipes_detected": len(all_recipes),
        "menu_items_detected": len(all_menu_items),
    }

    if not all_recipes and not all_menu_items:
        warnings.append("Workbook processed but no recipes or menu items were detected.")

    return {
        "recipes": all_recipes,
        "menu_items": all_menu_items,
        "metadata": metadata,
        "warnings": warnings,
    }


