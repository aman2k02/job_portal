// small script to toggle sidebar collapsed state on larger screens and show/hide on mobile
document.addEventListener('DOMContentLoaded', function(){
  const sidebar = document.getElementById('sidebar');
  // collapse on hover effect for md+ screens
  if (window.innerWidth >= 768) {
    sidebar.classList.add('collapsed');
    sidebar.addEventListener('mouseenter', ()=> sidebar.classList.remove('collapsed'));
    sidebar.addEventListener('mouseleave', ()=> sidebar.classList.add('collapsed'));
  }
  // toggle for mobile
  const toggle = document.getElementById('toggle');
  if (toggle) {
    toggle.addEventListener('click', ()=>{
      sidebar.classList.toggle('show');
    });
  }
});
