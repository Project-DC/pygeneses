// Select all the navbar tabs
const tabs = document.querySelectorAll('[data-tab-target]')

// Select all the displayable content
const tabContents = document.querySelectorAll('[data-tab-content]')

// Parse through the tabs to add or remove the active class to show the visibility
tabs.forEach(tab => {
  tab.addEventListener('click', () => {
    const target = document.querySelector(tab.dataset.tabTarget)
    tabContents.forEach(tabContent => {
      tabContent.classList.remove('active')
    })
    tabs.forEach(tab => {
      tab.classList.remove('active')
    })
    tab.classList.add('active')
    target.classList.add('active')
  })
})