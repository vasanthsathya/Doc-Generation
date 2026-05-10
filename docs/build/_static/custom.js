// Custom JavaScript for pydata-sphinx-theme

// Move search field to top row and create two-row navbar
document.addEventListener('DOMContentLoaded', function() {
  const headerInner = document.querySelector('.bd-header__inner');
  
  if (headerInner) {
    const startItems = headerInner.querySelector('.navbar-header-items__start');
    const endItems = headerInner.querySelector('.navbar-header-items__end');
    
    if (startItems && endItems) {
      // Move search field from end to start
      const searchField = endItems.querySelector('.search-field');
      if (searchField) {
        startItems.appendChild(searchField);
      }
    }
  }
});
