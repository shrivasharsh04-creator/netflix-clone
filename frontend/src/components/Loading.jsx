export default function Loading() {
  return (
    <div className="loading" aria-busy="true" aria-label="Loading">
      <div className="skeleton skeleton--hero" />
      {[1, 2, 3].map((n) => (
        <div key={n} className="skeleton-row">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="skeleton skeleton--card" />
          ))}
        </div>
      ))}
    </div>
  );
}
