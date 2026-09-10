from Game import SIZE

def bits_from_string(board_str: str) -> int:
    lines = [
        line.strip()
        for line in board_str.strip().splitlines()
        if line.strip()
    ]

    if any(len(line) > SIZE for line in lines) or len(lines) > SIZE:
        raise ValueError("Board invalido")

    bits = 0

    for row, line in enumerate(lines):
        for col, cell in enumerate(line):
            if cell == "X":
                bits |= 1 << (row * SIZE + col)
            elif cell != ".":
                raise ValueError(f"Célula inválida: {cell}")

    return bits