// Custom JavaScript for pydata-sphinx-theme

// Fetch GitHub repository data and update icon links with counts
document.addEventListener('DOMContentLoaded', function() {
  const headerInner = document.querySelector('.bd-header__inner');
  
  if (headerInner) {
    const startItems = headerInner.querySelector('.navbar-header-items__start');
    const endItems = headerInner.querySelector('.navbar-header-items__end');
    
    if (startItems && endItems) {
      // Add custom theme switch button first (before search)
      addThemeSwitchButton(startItems);
      
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

  // Fetch GitHub API data immediately after DOM manipulation is complete
  fetchGitHubData();
});

function addThemeSwitchButton(container) {
  // Create theme switch button container
  const themeSwitchContainer = document.createElement('div');
  themeSwitchContainer.className = 'navbar-item';
  
  const themeSwitchButton = document.createElement('button');
  themeSwitchButton.className = 'btn btn-sm nav-link theme-switch-button-custom';
  themeSwitchButton.setAttribute('aria-label', 'Color mode');
  themeSwitchButton.setAttribute('title', 'Toggle dark/light mode');
  themeSwitchButton.innerHTML = '<i class="fa-solid fa-moon"></i>';
  
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
    button.innerHTML = '<i class="fa-solid fa-moon"></i>';
    localStorage.setItem('theme', 'light');
  } else {
    html.setAttribute('data-theme', 'dark');
    button.innerHTML = '<i class="fa-solid fa-sun"></i>';
    localStorage.setItem('theme', 'dark');
  }
}

function setInitialTheme(button) {
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    document.documentElement.setAttribute('data-theme', 'dark');
    button.innerHTML = '<i class="fa-solid fa-sun"></i>';
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
    button.innerHTML = '<i class="fa-solid fa-moon"></i>';
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
  const githubLink = document.querySelector('.navbar-icon-links .nav-link[title="GitHub"]') ||
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
    
    const icon = document.createElement('i');
    icon.className = 'fa-brands fa-github github-main-icon';
    icon.style.fontSize = '1.8rem';
    icon.style.color = 'white';
    
    iconColumn.appendChild(icon);
    
    // Create info column with repo name only
    const infoColumn = document.createElement('div');
    infoColumn.className = 'github-info-column';
    
    const repoRow = document.createElement('div');
    repoRow.className = 'github-repo-row';
    
    const repoName = document.createElement('span');
    repoName.className = 'github-repo-name';
    repoName.textContent = 'dell/omnia';
    
    repoRow.appendChild(repoName);
    infoColumn.appendChild(repoRow);
    
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
  const githubLink = document.querySelector('.navbar-icon-links .nav-link[title="GitHub"]') ||
                       document.querySelector('.navbar-icon-links a[title="GitHub"]') ||
                       document.querySelector('.navbar-icon-links a.pst-navbar-icon[title="GitHub"]') ||
                       document.querySelector('.navbar-icon-links a[href*="github.com/dell/omnia"]') ||
                       document.querySelector('a[title="GitHub"][href*="github.com/dell/omnia"]');
  
  console.log('GitHub link found:', githubLink);
  console.log('Repo data:', repoData);
  console.log('Release data:', releaseData);
  
  if (githubLink) {
    // Create a container for the stacked layout
    const githubContainer = document.createElement('div');
    githubContainer.className = 'github-info-container';
    
    // Create GitHub icon column (left side)
    const iconColumn = document.createElement('div');
    iconColumn.className = 'github-icon-column';
    
    // Create GitHub icon directly instead of cloning
    const icon = document.createElement('i');
    icon.className = 'fa-brands fa-github github-main-icon';
    icon.style.fontSize = '1.8rem';
    icon.style.color = 'white';
    console.log('Created GitHub icon element:', icon);
    
    iconColumn.appendChild(icon);
    
    // Create info column (right side)
    const infoColumn = document.createElement('div');
    infoColumn.className = 'github-info-column';
    
    // Create repository name row
    const repoRow = document.createElement('div');
    repoRow.className = 'github-repo-row';
    
    const repoName = document.createElement('span');
    repoName.className = 'github-repo-name';
    repoName.textContent = 'dell/omnia';
    
    repoRow.appendChild(repoName);
    
    // Create stats row
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
    
    infoColumn.appendChild(repoRow);
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
  
  const statIcon = document.createElement('i');
  statIcon.className = iconClass;
  
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
