document.addEventListener("DOMContentLoaded", () => {
  const board = document.getElementById("board");
  const scrambleButton = document.getElementById("scramble-button");

  const size = 3;
  let tiles = [];
  let blankTile = { row: size - 1, col: size - 1 };
  let disableWinCheck = true; // Flag to control win check during initial scramble
  let moveCount = 0; // Initialize move counter

  // Initialize the board
  function initializeBoard() {
    tiles = Array.from({ length: size * size }, (_, i) => i + 1);
    tiles[tiles.length - 1] = ""; // Set the last tile as blank
    renderBoard();
	
	// Clear the win message each time the board is initialized or scrambled
    document.getElementById("win-message").textContent = "";
	
	// Scramble the board after setting up
    scrambleBoard();
  }

  // Render the board to HTML
  function renderBoard() {
    board.innerHTML = "";
    board.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
    tiles.forEach((value, index) => {
        const tile = document.createElement("div");
        
        // Apply classes based on whether the tile is in the correct position
        if (value === "") {
            tile.className = "tile blank"; // Blank tile styling
        } else if (value === index + 1) {
            tile.className = "tile correct"; // Correct position styling
        } else {
            tile.className = "tile incorrect"; // Incorrect position styling
        }
        
        tile.textContent = value;
        tile.dataset.index = index;
        tile.addEventListener("click", () => moveTile(index));
        board.appendChild(tile);
    });
	updateMoveCounter(); // Update move counter display each render
}

  // Move tile if adjacent to blank
  function moveTile(index) {
    const row = Math.floor(index / size);
    const col = index % size;
    const isAdjacent = 
      (row === blankTile.row && Math.abs(col - blankTile.col) === 1) ||
      (col === blankTile.col && Math.abs(row - blankTile.row) === 1);

    if (isAdjacent) {
      const blankIndex = blankTile.row * size + blankTile.col;
      [tiles[index], tiles[blankIndex]] = [tiles[blankIndex], tiles[index]];
      blankTile = { row, col };
	  if (!disableWinCheck) {
        moveCount++;
      }
      renderBoard();
      checkWin();
    }
  }

  // Scramble the board
  function scrambleBoard() {
	// Clear the win message each time the board is initialized or scrambled
    document.getElementById("win-message").textContent = "";  
	
	moveCount = 0;
	updateMoveCounter(); // Display the move counter

	// Disable win check during scrambling
	disableWinCheck = true; 
	  
    for (let i = 0; i < 10000; i++) {
      const direction = Math.floor(Math.random() * 4);
      let targetIndex;

      switch (direction) {
        case 0: targetIndex = blankTile.row > 0 ? (blankTile.row - 1) * size + blankTile.col : null; break; // UP
        case 1: targetIndex = blankTile.row < size - 1 ? (blankTile.row + 1) * size + blankTile.col : null; break; // DOWN
        case 2: targetIndex = blankTile.col > 0 ? blankTile.row * size + blankTile.col - 1 : null; break; // LEFT
        case 3: targetIndex = blankTile.col < size - 1 ? blankTile.row * size + blankTile.col + 1 : null; break; // RIGHT
      }

      if (targetIndex !== null) moveTile(targetIndex);
    }
	disableWinCheck = false; // Allow win check after scrambling completes
  }

  // Check if the board is in a solved state
  function checkWin() {
    if (!disableWinCheck && tiles.slice(0, -1).every((tile, i) => tile === i + 1)) {
        document.getElementById("win-message").textContent = "Congratulations! You solved the puzzle.";
    }
  }
  
  function updateMoveCounter() {
    document.getElementById("move-counter").textContent = `Moves: ${moveCount}`;
}

  // Event listeners for buttons
  scrambleButton.addEventListener("click", scrambleBoard);

  initializeBoard();
});