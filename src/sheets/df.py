import pandas as pd
import gspread
import gspread_dataframe
import os
from src.utils import print_info


def convert_to_dataframe(file_path: str) -> pd.DataFrame:
    _, extension = os.path.splitext(file_path)

    df = None
    if extension == ".csv":
        df = pd.read_csv(file_path)

    return df


def append_to_google_sheets(
    dataframe: pd.DataFrame,
    spreadsheet_id: str,
    credentials: str,
    sheet_name: str,
    unique_column: str = None,
):
    gc = gspread.service_account(filename=credentials)

    if sheet_name is None:
        wks = gc.open_by_key(spreadsheet_id).sheet1
    else:
        wks = gc.open_by_key(spreadsheet_id).worksheet(sheet_name)

    new_df = dataframe.copy()

    sheet_df = gspread_dataframe.get_as_dataframe(wks, evaluate_formulas=True, header=0)
    sheet_df = sheet_df.dropna(how="all")
    sheet_df = sheet_df.dropna(axis=1, how="all")

    if not sheet_df.empty:
        rows_to_append = new_df[~new_df[unique_column].isin(sheet_df[unique_column])]
    else:
        rows_to_append = new_df

    if not rows_to_append.empty:
        first_empty_row = len(wks.col_values(1)) + 1
        gspread_dataframe.set_with_dataframe(
            wks,
            rows_to_append,
            row=first_empty_row,
            col=1,
            include_index=False,
            include_column_header=first_empty_row == 1,
        )
    else:
        print_info("No new matches to append.")
