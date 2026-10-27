import { useEffect, useState } from "react";
import { fetchTitle } from "../services/api";

export default function TitleModal({ id, onClose }) {
  const [title, setTitle] = useState(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    setTitle(null);
    setFailed(false);
    fetchTitle(id).then(setTitle).catch(() => setFailed(true));
  }, [id]);

  useEffect(() => {
    const onKey = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [onClose]);

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        onClick={(e) => e.stopPropagation()}
      >
        <button className="modal__close" aria-label="Close" onClick={onClose}>
          ×
        </button>
        {failed && <p className="modal__msg">Could not load this title. Try again.</p>}
        {!title && !failed && <p className="modal__msg">Loading…</p>}
        {title && (
          <>
            <div
              className="modal__banner"
              style={{ backgroundImage: `url(${title.backdrop_url})` }}
            >
              <div className="modal__fade" />
              <h2>{title.name}</h2>
            </div>
            <div className="modal__body">
              <p className="hero__meta">
                {title.rating && <span className="rating">{title.rating} / 10</span>}
                {title.year && <span>{title.year}</span>}
                {title.genres.map((g) => (
                  <span key={g}>{g}</span>
                ))}
              </p>
              <p>{title.overview}</p>
              {title.official_site && (
                <a
                  className="btn btn--light"
                  href={title.official_site}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  ▶ Official site
                </a>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
