import { useEffect, useState } from "react";

const LINKS = ["Home", "TV Shows", "New & Popular", "My List"];

export default function Navbar() {
  const [solid, setSolid] = useState(false);

  useEffect(() => {
    const onScroll = () => setSolid(window.scrollY > 40);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header className={`navbar ${solid ? "navbar--solid" : ""}`}>
      <span className="logo">NETFLIX</span>
      <nav className="nav-links">
        {LINKS.map((label, i) => (
          <a key={label} href="#" className={i === 0 ? "active" : ""}>
            {label}
          </a>
        ))}
      </nav>
    </header>
  );
}
