// Custom JavaScript for pydata-sphinx-theme

// Navbar scroll hide/show behavior
let lastScrollTop = 0;
let scrollTimeout;

document.addEventListener('DOMContentLoaded', function() {
  // Force sidebar to always be visible on wide screens
  forceSidebarVisible();
  
  // Also run after a short delay to ensure theme JS has loaded
  setTimeout(forceSidebarVisible, 500);

  const header = document.querySelector('.bd-header');
  
  if (header) {
    window.addEventListener('scroll', function() {
      const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      // Clear previous timeout
      clearTimeout(scrollTimeout);
      
      // Add small delay to prevent flickering
      scrollTimeout = setTimeout(function() {
        if (currentScrollTop > lastScrollTop && currentScrollTop > 100) {
          // Scrolling down - hide navbar
          header.classList.add('nav-hidden');
          header.classList.remove('nav-visible');
        } else {
          // Scrolling up - show navbar
          header.classList.remove('nav-hidden');
          header.classList.add('nav-visible');
        }
        lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop;
      }, 10);
    }, false);
  }
  
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
      
      // Add theme switch button (between search and github)
      addThemeSwitchButton(startItems);
      
      // Move repository icon links container from end to start
      const iconLinks = endItems.querySelector('.navbar-icon-links');
      if (iconLinks) {
        const iconLinksContainer = iconLinks.closest('.navbar-item');
        if (iconLinksContainer) {
          startItems.appendChild(iconLinksContainer);
        }
      }

      
      // Hide the now-empty end items container
      endItems.style.display = 'none';
    }
  }

  // Fetch GitHub API data immediately after DOM manipulation is complete
  fetchGitHubData();
  
  // Move prev/next footer to above copyright footer
  movePrevNextFooter();
  
  // Add GitHub logo to copyright footer
  addFooterGitHubLink();
});

function addThemeSwitchButton(container) {
  // Create theme switch button container
  const themeSwitchContainer = document.createElement('div');
  themeSwitchContainer.className = 'navbar-item';
  
  const themeSwitchButton = document.createElement('button');
  themeSwitchButton.className = 'btn btn-sm nav-link theme-switch-button-custom';
  themeSwitchButton.setAttribute('aria-label', 'Color mode');
  themeSwitchButton.setAttribute('title', 'Toggle dark/light mode');
  // Use SVG icon instead of FontAwesome with increased size for better readability
  themeSwitchButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="34" height="34" fill="white"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-3.03 0-5.5-2.47-5.5-5.5 0-1.82.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/></svg>`;
  
  // Add click handler to toggle theme
  themeSwitchButton.addEventListener('click', function() {
    toggleTheme(themeSwitchButton);
  });
  
  themeSwitchContainer.appendChild(themeSwitchButton);
  container.appendChild(themeSwitchContainer);
  
  // Set initial theme based on preference
  setInitialTheme(themeSwitchButton);
}

function toggleTheme(button) {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme');
  
  if (currentTheme === 'dark') {
    html.setAttribute('data-theme', 'light');
    // Moon icon for light mode (opposite behavior)
    button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="34" height="34" fill="white"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-3.03 0-5.5-2.47-5.5-5.5 0-1.82.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/></svg>`;
    localStorage.setItem('theme', 'light');
  } else {
    html.setAttribute('data-theme', 'dark');
    // Sun icon for dark mode (opposite behavior)
    button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="34" height="34" fill="white"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>`;
    localStorage.setItem('theme', 'dark');
  }
}

function setInitialTheme(button) {
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    document.documentElement.setAttribute('data-theme', 'dark');
    // Sun icon for dark mode (opposite behavior)
    button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="34" height="34" fill="white"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>`;
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
    // Moon icon for light mode (opposite behavior)
    button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="34" height="34" fill="white"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-3.03 0-5.5-2.47-5.5-5.5 0-1.82.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/></svg>`;
  }
}

async function fetchGitHubData() {
  try {
    console.log('Fetching GitHub data...');
    
    // Show basic GitHub icon immediately while loading
    showBasicGitHubIcon();
    
    // Fetch repository data and release data in parallel
    const [repoResponse, releaseResponse] = await Promise.all([
      fetch('https://api.github.com/repos/dell/omnia'),
      fetch('https://api.github.com/repos/dell/omnia/releases/latest')
    ]);
    
    const repoData = await repoResponse.json();
    const releaseData = await releaseResponse.json();
    
    console.log('GitHub data fetched:', repoData, releaseData);
    
    // Update GitHub link with repository info and stats
    updateGitHubLink(repoData, releaseData);
  } catch (error) {
    console.error('Error fetching GitHub data:', error);
  }
}

function showBasicGitHubIcon() {
  const githubLink = document.querySelector('.navbar-icon-links .nav-link.pst-navbar-icon[title="GitHub"]') ||
                       document.querySelector('.navbar-icon-links .nav-link[title="GitHub"]') ||
                       document.querySelector('.navbar-icon-links a[title="GitHub"]') ||
                       document.querySelector('.navbar-icon-links a.pst-navbar-icon[title="GitHub"]') ||
                       document.querySelector('.navbar-icon-links a[href*="github.com/dell/omnia"]') ||
                       document.querySelector('a[title="GitHub"][href*="github.com/dell/omnia"]');
  
  if (githubLink) {
    // Create a container for the basic icon
    const githubContainer = document.createElement('div');
    githubContainer.className = 'github-info-container';
    
    // Create GitHub icon column
    const iconColumn = document.createElement('div');
    iconColumn.className = 'github-icon-column';
    
    const icon = document.createElement('div');
    icon.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="white"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>`;
    icon.style.fontSize = '18px';
    icon.style.color = 'white';
    
    iconColumn.appendChild(icon);
    
    // Create info column with repo name only
    const infoColumn = document.createElement('div');
    infoColumn.className = 'github-info-column';
    
    const repoName = document.createElement('div');
    repoName.className = 'github-repo-name';
    repoName.textContent = 'dell/omnia';
    
    infoColumn.appendChild(repoName);
    
    githubContainer.appendChild(iconColumn);
    githubContainer.appendChild(infoColumn);
    
    // Clear the original link content and replace with our container
    githubLink.innerHTML = '';
    githubLink.appendChild(githubContainer);
    
    console.log('Basic GitHub icon shown');
  }
}

function updateGitHubLink(repoData, releaseData) {
  // Try multiple selectors to find the GitHub link
  const githubLink = document.querySelector('.navbar-icon-links .nav-link.pst-navbar-icon[title="GitHub"]') ||
                       document.querySelector('.navbar-icon-links .nav-link[title="GitHub"]') ||
                       document.querySelector('.navbar-icon-links a[title="GitHub"]') ||
                       document.querySelector('.navbar-icon-links a.pst-navbar-icon[title="GitHub"]') ||
                       document.querySelector('.navbar-icon-links a[href*="github.com/dell/omnia"]') ||
                       document.querySelector('a[title="GitHub"][href*="github.com/dell/omnia"]');
  
  console.log('GitHub link found:', githubLink);
  console.log('Repo data:', repoData);
  console.log('Release data:', releaseData);
  
  if (githubLink) {
    // Create a container for the layout
    const githubContainer = document.createElement('div');
    githubContainer.className = 'github-info-container';
    
    // Create GitHub icon column (left side)
    const iconColumn = document.createElement('div');
    iconColumn.className = 'github-icon-column';
    
    // Create GitHub icon directly instead of cloning
    const icon = document.createElement('div');
    icon.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="white"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>`;
    icon.style.fontSize = '18px';
    icon.style.color = 'white';
    console.log('Created GitHub icon element:', icon);
    
    iconColumn.appendChild(icon);
    
    // Create info column (right side) - single row with repo name, stats on next line
    const infoColumn = document.createElement('div');
    infoColumn.className = 'github-info-column';
    
    // Repository name (first line)
    const repoName = document.createElement('div');
    repoName.className = 'github-repo-name';
    repoName.textContent = 'dell/omnia';
    infoColumn.appendChild(repoName);
    
    // Stats (version, stars, forks) - second line
    const statsRow = document.createElement('div');
    statsRow.className = 'github-stats-row';
    
    // Version
    if (releaseData && releaseData.tag_name !== undefined) {
      const versionStat = createStatItem('fa-solid fa-tag', releaseData.tag_name, 'https://github.com/dell/omnia/releases');
      statsRow.appendChild(versionStat);
      console.log('Added version:', releaseData.tag_name);
    } else {
      console.log('No release data available');
    }
    
    // Stars
    if (repoData && repoData.stargazers_count !== undefined) {
      const starsStat = createStatItem('fa-solid fa-star', formatNumber(repoData.stargazers_count), 'https://github.com/dell/omnia/stargazers');
      statsRow.appendChild(starsStat);
      console.log('Added stars:', repoData.stargazers_count);
    } else {
      console.log('No star count available');
    }
    
    // Forks
    if (repoData && repoData.forks_count !== undefined) {
      const forksStat = createStatItem('fa-solid fa-code-fork', formatNumber(repoData.forks_count), 'https://github.com/dell/omnia/network/members');
      statsRow.appendChild(forksStat);
      console.log('Added forks:', repoData.forks_count);
    } else {
      console.log('No fork count available');
    }
    
    infoColumn.appendChild(statsRow);
    
    githubContainer.appendChild(iconColumn);
    githubContainer.appendChild(infoColumn);
    
    // Clear the original link content and replace with our container
    githubLink.innerHTML = '';
    githubLink.appendChild(githubContainer);
    
    console.log('GitHub link updated successfully');
  } else {
    console.error('GitHub link not found');
  }
}

function createStatItem(iconClass, text, url) {
  const statItem = document.createElement('a');
  statItem.href = url;
  statItem.className = 'github-stat-item';
  statItem.target = '_blank';
  statItem.rel = 'noopener';
  
  // Create SVG icon based on iconClass
  let svgIcon = '';
  if (iconClass.includes('fa-tag')) {
    svgIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="11" height="11" fill="white"><path d="M21.41 11.58l-9-9C12.05 2.22 11.55 2 11 2H4c-1.1 0-2 .9-2 2v7c0 .55.22 1.05.59 1.42l9 9c.36.36.86.58 1.41.58.55 0 1.05-.22 1.41-.59l7-7c.37-.36.59-.86.59-1.41 0-.55-.23-1.06-.59-1.42zM5.5 7C4.67 7 4 6.33 4 5.5S4.67 4 5.5 4 7 4.67 7 5.5 6.33 7 5.5 7z"/></svg>`;
  } else if (iconClass.includes('fa-star')) {
    svgIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="11" height="11" fill="white"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>`;
  } else if (iconClass.includes('fa-code-fork')) {
    svgIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="11" height="11" fill="white"><path d="M6 2c-1.1 0-2 .9-2 2s.9 2 2 2c.55 0 1.05-.22 1.41-.59l4.59 4.59c-.37.36-.59.86-.59 1.41 0 1.1.9 2 2 2s2-.9 2-2c0-.55-.22-1.05-.59-1.41L12 9.17 7.41 4.59C7.77 4.23 7.55 3.73 7.55 3.18c0-1.1-.9-2-2-2zM18 2c-1.1 0-2 .9-2 2s.9 2 2 2c.55 0 1.05-.22 1.41-.59L12 9.17 7.41 4.59C7.77 4.23 7.55 3.73 7.55 3.18c0-1.1-.9-2-2-2z"/></svg>`;
  }
  
  const statIcon = document.createElement('div');
  statIcon.innerHTML = svgIcon;
  
  const statText = document.createElement('span');
  statText.className = 'github-stat-text';
  statText.textContent = text;
  
  statItem.appendChild(statIcon);
  statItem.appendChild(statText);
  
  return statItem;
}

function formatNumber(num) {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k';
  }
  return num.toString();
}

// Force sidebar to always be visible on wide screens
function forceSidebarVisible() {
  const sidebar = document.getElementById('pst-primary-sidebar');
  if (sidebar) {
    // Remove the hide-on-wide class
    sidebar.classList.remove('hide-on-wide');
    
    // Use a MutationObserver to prevent the class from being added back
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (mutation.attributeName === 'class') {
          const target = mutation.target;
          if (target.classList.contains('hide-on-wide')) {
            target.classList.remove('hide-on-wide');
          }
        }
      });
    });
    
    observer.observe(sidebar, { attributes: true, attributeFilter: ['class'] });
  }
  
  // Hide the collapse button
  const collapseButton = document.getElementById('pst-collapse-sidebar-button');
  if (collapseButton) {
    collapseButton.style.display = 'none';
  }
  
  // Force all navigation items to be expanded
  const navItems = document.querySelectorAll('.bd-sidebar-primary .toctree-l1, .bd-sidebar-primary .toctree-l2, .bd-sidebar-primary .toctree-l3, .bd-sidebar-primary .toctree-l4');
  navItems.forEach(function(item) {
    item.style.display = 'block';
  });
}

// Move prev/next footer to above copyright footer
function movePrevNextFooter() {
  const prevNextFooter = document.querySelector('.prev-next-footer');
  const copyrightFooter = document.querySelector('.bd-footer');
  
  if (prevNextFooter && copyrightFooter) {
    // Remove the prev/next footer from its current location
    prevNextFooter.remove();
    
    // Insert it just before the copyright footer
    copyrightFooter.parentNode.insertBefore(prevNextFooter, copyrightFooter);
    
    // Ensure full-width styling
    prevNextFooter.style.width = '100%';
    prevNextFooter.style.position = 'relative';
    prevNextFooter.style.left = '0';
    prevNextFooter.style.right = '0';
    
    console.log('Prev/next footer moved above copyright footer with full-width styling');
  } else {
    console.log('Prev/next footer or copyright footer not found');
  }
}

// Add GitHub logo to copyright footer
function addFooterGitHubLink() {
  const footerInner = document.querySelector('.bd-footer .bd-footer__inner');
  const footerItemsEnd = document.querySelector('.bd-footer .footer-items__end');
  
  if (footerInner && footerItemsEnd) {
    // Clear any existing content in the end items
    footerItemsEnd.innerHTML = '';
    
    // Ensure the end items container is properly styled
    footerItemsEnd.style.flex = '0 0 auto';
    footerItemsEnd.style.marginLeft = 'auto';
    
    // Create GitHub link container
    const githubContainer = document.createElement('div');
    githubContainer.className = 'footer-item';
    githubContainer.style.display = 'flex';
    githubContainer.style.alignItems = 'center';
    
    const githubLink = document.createElement('a');
    githubLink.href = 'https://github.com/dell/omnia';
    githubLink.className = 'footer-github-link';
    githubLink.target = '_blank';
    githubLink.rel = 'noopener';
    
    // GitHub SVG icon
    githubLink.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="1.5rem" height="1.5rem" fill="white">
        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
      </svg>
      <span>GitHub</span>
    `;
    
    githubContainer.appendChild(githubLink);
    
    // Add to the end items section
    footerItemsEnd.appendChild(githubContainer);
    
    console.log('GitHub link added to footer');
  } else {
    console.log('Footer inner or end items not found');
  }
}

