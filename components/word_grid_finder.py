from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Message
import json
import re


class WordGridFinderComponent(Component):
    display_name = "Word Grid Finder"
    description = "Finds words in a 2D letter grid and generates HTML visualization"
    icon = "grid-3x3"

    inputs = [
        MessageTextInput(
            name="grid_json",
            display_name="Letter Grid (JSON)",
            info="2D array of letters as JSON string",
        ),
        MessageTextInput(
            name="word_list",
            display_name="Word List",
            info="Words to find (can be messy AI text)",
        ),
    ]

    outputs = [
        Output(type=Message, display_name="HTML", name="html_output", method="find_words"),
    ]

    # 8 directions
    DIRECTIONS = [
        (0,1),(1,0),(0,-1),(-1,0),
        (1,1),(1,-1),(-1,1),(-1,-1)
    ]


    # ---------- SAFE WORD SEARCH ----------
    def find_word_in_grid(self, grid, word):
        rows = len(grid)

        for r in range(rows):
            for c in range(len(grid[r])):
                if grid[r][c] != word[0]:
                    continue

                for dr, dc in self.DIRECTIONS:
                    positions = []
                    rr, cc = r, c

                    for letter in word:
                        if (
                            0 <= rr < rows and
                            0 <= cc < len(grid[rr]) and
                            grid[rr][cc] == letter
                        ):
                            positions.append((rr, cc))
                            rr += dr
                            cc += dc
                        else:
                            break
                    else:
                        return positions

        return []


    # ---------- MAIN ----------
    def find_words(self) -> Message:
        try:
            grid = json.loads(self.grid_json)
            grid = [[cell.upper() for cell in row] for row in grid]

            # SMART WORD EXTRACTION (handles LLM text)
            raw_words = re.findall(r"[A-Za-z]{3,}", self.word_list.upper())

            seen = set()
            words = []
            for w in raw_words:
                if w not in seen:
                    seen.add(w)
                    words.append(w)

            # detect jagged grid
            row_lengths = [len(r) for r in grid]
            jagged_warning = ""
            if len(set(row_lengths)) != 1:
                jagged_warning = f"<div style='color:orange;font-weight:bold;'>Warning: Uneven row lengths detected → {row_lengths}</div>"

            all_positions = {}
            found_words = []
            missing_words = []

            for word in words:
                positions = self.find_word_in_grid(grid, word)
                if positions:
                    all_positions[word] = positions
                    found_words.append(word)
                else:
                    missing_words.append(word)

            html = jagged_warning + self.generate_html(grid, all_positions, found_words, missing_words)
            return Message(text=html)

        except Exception as e:
            return Message(text=f"<div style='color:red;font-weight:bold;'>Error: {str(e)}</div>")


    # ---------- HTML ----------
    def generate_html(self, grid, positions_dict, found_words, missing_words):

        highlighted = set()
        for pos in positions_dict.values():
            highlighted.update(pos)

        html = """
        <div style="font-family:Arial">
        <h2>Word Search Result</h2>
        <table style="border-collapse: collapse; font-size:20px;">
        """

        for r in range(len(grid)):
            html += "<tr>"
            for c in range(len(grid[r])):
                if (r,c) in highlighted:
                    html += f'<td style="border:1px solid #999;padding:8px;background:#4CAF50;color:white;font-weight:bold;text-align:center;">{grid[r][c]}</td>'
                else:
                    html += f'<td style="border:1px solid #999;padding:8px;background:#f3f3f3;text-align:center;">{grid[r][c]}</td>'
            html += "</tr>"

        html += "</table>"

        html += "<h3 style='color:green;'>Found Words:</h3><ul>"
        for w in found_words:
            html += f"<li>{w}</li>"
        html += "</ul>"

        if missing_words:
            html += "<h3 style='color:red;'>Not Found:</h3><ul>"
            for w in missing_words:
                html += f"<li>{w}</li>"
            html += "</ul>"

        html += "</div>"
        return html