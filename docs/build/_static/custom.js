// Custom JavaScript for pydata-sphinx-theme

// Move search field and repository icon to top row
document.addEventListener('DOMContentLoaded', function() {
  const headerInner = document.querySelector('.bd-header__inner');
  
  if (headerInner) {
    const startItems = headerInner.querySelector('.navbar-header-items__start');
    const endItems = headerInner.querySelector('.navbar-header-items__end');
    
    if (startItems && endItems) {
      // Move search button container from end to start
      const searchContainer = endItems.querySelector('.navbar-persistent--container');
      if (searchContainer) {
        startItems.appendChild(searchContainer);
      }
      
      // Move repository icon links container from end to start
      const iconLinks = endItems.querySelector('.navbar-icon-links');
      if (iconLinks) {
        const iconLinksContainer = iconLinks.closest('.navbar-item');
        if (iconLinksContainer) {
          startItems.appendChild(iconLinksContainer);
        }
      }
    }
  }
});
