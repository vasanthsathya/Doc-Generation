// Custom JavaScript for pydata-sphinx-theme

// Restructure navbar into two rows
document.addEventListener('DOMContentLoaded', function() {
  const header = document.querySelector('.bd-header');
  const headerInner = document.querySelector('.bd-header__inner');
  
  if (header && headerInner) {
    // Get the navbar elements
    const startItems = headerInner.querySelector('.navbar-header-items__start');
    const centerItems = headerInner.querySelector('.navbar-header-items__center');
    const endItems = headerInner.querySelector('.navbar-header-items__end');
    
    if (startItems && centerItems) {
      // Create top row with logo and search
      const topRow = document.createElement('div');
      topRow.className = 'navbar-top-row';
      
      // Clone the start items (logo and sidebar toggle)
      const startClone = startItems.cloneNode(true);
      topRow.appendChild(startClone);
      
      // Add search to top row if available
      const searchField = endItems ? endItems.querySelector('.search-field') : null;
      if (searchField) {
        const searchContainer = document.createElement('div');
        searchContainer.className = 'navbar-search-container';
        searchContainer.appendChild(searchField);
        topRow.appendChild(searchContainer);
      }
      
      // Create bottom row with navigation menu
      const bottomRow = document.createElement('div');
      bottomRow.className = 'navbar-bottom-row';
      
      // Clone the center items (navigation menu)
      const centerClone = centerItems.cloneNode(true);
      bottomRow.appendChild(centerClone);
      
      // Clear the original header inner
      headerInner.innerHTML = '';
      
      // Add the new rows
      headerInner.appendChild(topRow);
      headerInner.appendChild(bottomRow);
      
      // Remove the original elements
      startItems.remove();
      centerItems.remove();
    }
  }
});
