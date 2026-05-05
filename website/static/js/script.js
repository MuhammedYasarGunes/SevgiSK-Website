/* ─────────────────────────────────────────
   NAVBAR – Mobile Menu Toggle
───────────────────────────────────────── */
const menuToggle = document.getElementById('menuToggle');
const navLinks   = document.getElementById('navLinks');
 
if (menuToggle && navLinks) {
 
  menuToggle.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = navLinks.classList.toggle('active');
    menuToggle.classList.toggle('active', isOpen);
  });
 
  // Link tıklandığında menüyü kapat + aktif linki işaretle
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      closeMenu();
      document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
      link.classList.add('active');
    });
  });
 
  // Navbar dışına tıklanınca kapat
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.navbar')) closeMenu();
  });
 
  // ESC tuşuyla kapat
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMenu();
  });
}
 
function closeMenu() {
  menuToggle?.classList.remove('active');
  navLinks?.classList.remove('active');
  // NOT: .display class'ı CSS'den kaldırıldığı için burada dokunmuyoruz
}
 
// Sayfa yüklenince mevcut URL'e göre aktif linki belirle
(function setActiveLink() {
  const current = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href')?.split('/').pop();
    link.classList.toggle('active', href === current);
  });
})();

// Close menu when clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.navbar') && !e.target.closest('.nav-links')) {
    menuToggle.classList.remove('active');
    navLinks.classList.remove('active');
    navLinks.classList.remove('display'); // ← EKLENDİ
  }
});

