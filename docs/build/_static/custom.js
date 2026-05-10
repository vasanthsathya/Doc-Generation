// Custom JavaScript for sphinx-rtd-theme

// Add custom top navigation bar
document.addEventListener('DOMContentLoaded', function() {
  // Create the navigation bar
  const navBar = document.createElement('div');
  navBar.className = 'custom-top-nav';
  
  // Create logo link
  const logoLink = document.createElement('a');
  logoLink.href = 'index.html';
  logoLink.className = 'logo-link';
  logoLink.innerHTML = '<img src="_static/omnia-logo.png" alt="Logo" /> Dell Omnia';
  
  // Create nav links container
  const navLinks = document.createElement('div');
  navLinks.className = 'nav-links';
  
  // Add navigation links
  const links = [
    { href: 'Overview/index.html', text: 'Overview' },
    { href: 'GetStarted/index.html', text: 'Get Started' },
    { href: 'HowTo/index.html', text: 'How-to Guides' },
    { href: 'Operations/index.html', text: 'Operations' },
    { href: 'Reference/index.html', text: 'Reference' },
    { href: 'Troubleshooting/index.html', text: 'Troubleshooting' },
    { href: 'Contributing/index.html', text: 'Contributing' }
  ];
  
  links.forEach(link => {
    const a = document.createElement('a');
    a.href = link.href;
    a.textContent = link.text;
    navLinks.appendChild(a);
  });
  
  // Assemble the navigation bar
  navBar.appendChild(logoLink);
  navBar.appendChild(navLinks);
  
  // Insert at the beginning of body
  const body = document.body;
  body.insertBefore(navBar, body.firstChild);
});
