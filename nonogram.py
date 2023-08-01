from PIL import Image, ImageDraw, ImageFont

class Sentence():
    """
    Logical statement about a nonogram puzzle
    It consists of a list of clues, length, direction
    and a starting point.
    """
    
    
    def __init__(self, clues, length, start) -> None:
        self.clues = clues
        self.length = length
        self.start = start
        self.min_length = len(clues) - 1
        for clue in clues:
            self.min_length += clue
    
    def __eq__(self, other) -> bool:
        return self.clues == other.clues and self.length == other.length and self.start == other.start
    
    def __str__(self) -> str:
        return f"{self.clues}"
    
    def __hash__(self) -> int:
        return hash(tuple(self.clues)) + self.length * 21
    
    
class Nonogram():
    """
    Nonogram puzzle representation.
    """
    def __init__(self, height, width, ver_clues, hor_clues) -> None:
        self.height = height
        self.width = width
        self.ver_clues = ver_clues
        self.hor_clues = hor_clues
        # Create an empty puzzle. 
        self.puzzle = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(None)
            self.puzzle.append(row)
        
        
        self.ver_knowledge = set()
        self.hor_knowledge = set()

        # Add knowledge based on the given clues.
        for i in range(len(ver_clues)):
            self.ver_knowledge.add(Sentence(ver_clues[i], self.height, (0, i)))
        
        for i in range(len(hor_clues)):
            self.hor_knowledge.add(Sentence(hor_clues[i], self.width, (i, 0)))
    
    def __hash__(self) -> int:
        return hash(tuple(self.ver_clues)) + hash(tuple(self.ver_clues)) + self.height * self.width * 2
        
    def solve(self):
        while len(self.ver_knowledge) != 0 and len(self.hor_knowledge) != 0:
            finished_sentences_ver = set()
            new_sentences_var = set()
            for sentence in self.ver_knowledge:
                # Check if all the cells in the sentence are full.
                full = True
                x, y = sentence.start
                for n in range(sentence.length):
                    if self.puzzle[x+n][y] == None:
                        full = False
                        break
                if full:
                    finished_sentences_ver.add(sentence)
                
                # Only one possibility. Fill the board accordingly.
                elif sentence.min_length == sentence.length:
                    i, j = sentence.start
                    for clue in sentence.clues:
                        for n in range(clue):
                            self.puzzle[i][j] = True
                            i += 1
                        if i < sentence.length + sentence.start[0]:
                            self.puzzle[i][j] = False
                            i += 1
                
                # Border inference. 
                
                
            for sentence in finished_sentences_ver:
                self.ver_knowledge.remove(sentence)
            
            finished_sentences_hor = set()
            for sentence in self.hor_knowledge:
                full = True
                x, y = sentence.start
                for n in range(sentence.length):
                    if self.puzzle[x][y+n] == None:
                        full = False
                        break
                if full:
                    finished_sentences_hor.add(sentence)
                elif sentence.min_length == sentence.length:
                    i, j = sentence.start
                    for clue in sentence.clues:
                        for n in range(clue):
                            self.puzzle[i][j] = True
                            j += 1
                        if j < sentence.length + sentence.start[1]:
                            self.puzzle[i][j] = False
                            j += 1
            for sentence in finished_sentences_hor:
                self.hor_knowledge.remove(sentence)
    

def save_puzzle_as_image(nonogram, filename):
    # Extract puzzle board, vertical clues, and horizontal clues
    board = nonogram.puzzle
    ver_clues = nonogram.ver_clues
    hor_clues = nonogram.hor_clues

    # Determine the height and width of the board
    height = len(board)
    width = len(board[0])

    # Constants for image rendering
    cell_size = 100
    cell_border = 2
    interior_size = cell_size - 2 * cell_border

    # Load font
    font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)

    # Create a blank canvas for the image
    img_width = width * cell_size
    img_height = height * cell_size
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # Draw vertical clues (top of each column)
    ver_clues_max_length = max(len(clue) for clue in ver_clues)
    for i in range(ver_clues_max_length):
        clue_row_str = ' '.join(str(clue[i]) if i < len(clue) else ' ' for clue in ver_clues)
        w, h = draw.textsize(clue_row_str, font=font)
        draw.text(((img_width - w) // 2, i * cell_size + ((cell_size - h) // 2) - 10), clue_row_str, fill="black", font=font)

    # Draw horizontal line separator
    for i in range(width):
        draw.line([(i * cell_size, 0), (i * cell_size, img_height)], fill="black", width=2)

    # Draw the board with vertical clues on the left side of each row
    for i in range(height):
        row_str = ' '.join(str(clue) for clue in hor_clues[i])
        w, h = draw.textsize(row_str, font=font)
        draw.text((0, i * cell_size + ((cell_size - h) // 2) - 10), row_str, fill="black", font=font)
        for j in range(width):
            cell = board[i][j]
            rect = [
                (j * cell_size + cell_border, i * cell_size + cell_border),
                ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)
            ]
            draw.rectangle(rect, fill="black" if cell else "white")

    # Save the image to the specified file
    img.save(filename)


        

width = int(input("Enter the width: "))
height = int(input("Enter the height: "))
ver_clues = []
for i in range(width):
    clue = input("Enter vertical clues: ")
    clues = clue.split(" ")
    clues = [int(i) for i in clues]
    ver_clues.append(clues)

hor_clues = []
for i in range(height):
    clue = input("Enter horizontal clues: ")
    clues = clue.split()
    clues = [int(i) for i in clues]
    hor_clues.append(clues)

nonogram = Nonogram(width, height, ver_clues, hor_clues)
nonogram.solve()

save_puzzle_as_image(nonogram, "image.png")