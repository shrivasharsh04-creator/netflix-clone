export default function PosterCard({ title, onSelect }) {
  return (
    <button className="card" onClick={() => onSelect(title.id)}>
      <img src={title.poster_url} alt={title.name} loading="lazy" />
      <div className="card__info">
        <strong>{title.name}</strong>
        <span>
          {title.rating ? `★ ${title.rating}` : "Not rated"}
          {title.genres[0] ? ` · ${title.genres[0]}` : ""}
        </span>
      </div>
    </button>
  );
}
