from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import numpy as np

def draw_grid(c, start_x, start_y, grid_width, grid_height, column_titles, title_font_size):
    # Adjust cell size based on the grid size
    cell_width = grid_width / 5
    cell_height = grid_height / 7
    
    # Generate a 5x5 array with unique random numbers between 1 and 50
    unique_random_numbers = np.random.choice(range(1, 51), size=(5*5), replace=False)
    random_array = unique_random_numbers.reshape((5, 5))

    # Draw column titles and adjust for the cell size
    c.setFont("Helvetica-Bold", title_font_size)
    for i, title in enumerate(column_titles):
        title_x = start_x + i * cell_width + (cell_width - c.stringWidth(title, "Helvetica-Bold", title_font_size)) / 2
        c.drawString(title_x, start_y + grid_height - cell_height/2, title)

    # Draw the grid and fill in the numbers
    c.setFont("Helvetica-Bold", 15)  # Adjust font size for better fit in the cell
    for row in range(5):
        for col in range(5):
            x = start_x + col * cell_width
            y = start_y + grid_height - (row + 1) * cell_height - cell_height
            c.rect(x, y, cell_width, cell_height)
            content = str(random_array[row, col])
            text_width = c.stringWidth(content, "Helvetica-Bold", 15)
            c.drawString(x + (cell_width - text_width) / 2, y + cell_height / 2 - 4, content)

def draw_separation_lines(c, width, height, grids_per_page):
    if grids_per_page == 4:
        # Draw horizontal line
        c.line(0, height/2, width, height/2)
        # Draw vertical line
        c.line(width/2, 0, width/2, height)

# Configuration for the PDF and grid
pdf_file_path = "grids_a4.pdf"
c = canvas.Canvas(pdf_file_path, pagesize=A4)
width, height = A4

# Number of grids per page and total number of grids
grids_per_page = 4  # Can be adjusted as needed
total_grids = 580  # Total number of grids to generate

column_titles = ["F", "I", "NN", "G", "O"]
title_font_size = 15

# Calculate grid size and margins
grid_width = width / 2
grid_height = height / 2
margin = grid_width / 10  # Dynamic margin based on grid width

for grid_number in range(total_grids):
    if grid_number % grids_per_page == 0 and grid_number != 0:
        c.showPage()  # Add a new page for the next set of grids
        draw_separation_lines(c, width, height, grids_per_page)

    quadrant = grid_number % grids_per_page
    start_x = margin + (quadrant % 2) * grid_width
    start_y = height - ((quadrant // 2) + 1) * (30*grid_height/29) + margin

    draw_grid(c, start_x, start_y, grid_width - 2*margin, grid_height - 2*margin, column_titles, title_font_size)

    # Ensure separation lines are drawn on the first page as well
    if grid_number == 0:
        draw_separation_lines(c, width, height, grids_per_page)

c.save()

print(f"Saved {total_grids} grids with unique numbers and column titles, {grids_per_page} per page, to '{pdf_file_path}' successfully.")