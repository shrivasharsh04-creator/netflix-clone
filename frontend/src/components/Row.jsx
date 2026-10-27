import { useRef } from "react";
import PosterCard from "./PosterCard";

export default function Row({ row, onSelect }) {
  const scroller = useRef(null);

  const scroll = (direction) => {
    const el = scroller.current;
    el.scrollBy({ left: direction * el.clientWidth * 0.85, behavior: "smooth" });
  };

  return (
    <section className="row">
      <h2>{row.display_name}</h2>
      {row.titles.length === 0 ? (
        <p className="empty">No titles in this row yet.</p>
      ) : (
        <div className="row__wrap">
          <button
            className="row__arrow row__arrow--left"
            aria-label={`Scroll ${row.display_name} left`}
            onClick={() => scroll(-1)}
          >
            ‹
          </button>
          <div className="row__scroller" ref={scroller}>
            {row.titles.map((t) => (
              <PosterCard key={t.id} title={t} onSelect={onSelect} />
            ))}
          </div>
          <button
            className="row__arrow row__arrow--right"
            aria-label={`Scroll ${row.display_name} right`}
            onClick={() => scroll(1)}
          >
            ›
          </button>
        </div>
      )}
    </section>
  );
}
