// Custom JavaScript for pydata-sphinx-theme

// Fetch GitHub repository data and update icon links with counts
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

  // Fetch GitHub API data
  fetchGitHubData();
});

async function fetchGitHubData() {
  try {
    // Fetch repository data
    const repoResponse = await fetch('https://api.github.com/repos/dell/omnia');
    const repoData = await repoResponse.json();
    
    // Fetch latest release data
    const releaseResponse = await fetch('https://api.github.com/repos/dell/omnia/releases/latest');
    const releaseData = await releaseResponse.json();
    
    // Update GitHub link with repository info and stats
    updateGitHubLink(repoData, releaseData);
  } catch (error) {
    console.error('Error fetching GitHub data:', error);
  }
}

function updateGitHubLink(repoData, releaseData) {
  const githubLink = document.querySelector('.navbar-icon-links .nav-link[title="GitHub"]');
  
  if (githubLink) {
    // Create a container for the stacked layout
    const githubContainer = document.createElement('div');
    githubContainer.className = 'github-info-container';
    
    // Create repository name row
    const repoRow = document.createElement('div');
    repoRow.className = 'github-repo-row';
    
    const icon = githubLink.querySelector('i');
    const repoName = document.createElement('span');
    repoName.className = 'github-repo-name';
    repoName.textContent = 'dell/omnia';
    
    repoRow.appendChild(icon.cloneNode(true));
    repoRow.appendChild(repoName);
    
    // Create stats row
    const statsRow = document.createElement('div');
    statsRow.className = 'github-stats-row';
    
    // Version
    if (releaseData.tag_name !== undefined) {
      const versionStat = createStatItem('fa-solid fa-tag', releaseData.tag_name, 'https://github.com/dell/omnia/releases');
      statsRow.appendChild(versionStat);
    }
    
    // Stars
    if (repoData.stargazers_count !== undefined) {
      const starsStat = createStatItem('fa-solid fa-star', formatNumber(repoData.stargazers_count), 'https://github.com/dell/omnia/stargazers');
      statsRow.appendChild(starsStat);
    }
    
    // Forks
    if (repoData.forks_count !== undefined) {
      const forksStat = createStatItem('fa-solid fa-code-fork', formatNumber(repoData.forks_count), 'https://github.com/dell/omnia/network/members');
      statsRow.appendChild(forksStat);
    }
    
    githubContainer.appendChild(repoRow);
    githubContainer.appendChild(statsRow);
    
    // Clear the original link content and replace with our container
    githubLink.innerHTML = '';
    githubLink.appendChild(githubContainer);
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
