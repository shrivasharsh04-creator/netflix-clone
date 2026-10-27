export default function HeroBanner({ hero, onMoreInfo }) {
  if (!hero) return null;

  const play = () => {
    if (hero.official_site) window.open(hero.official_site, "_blank", "noopener");
    else onMoreInfo(hero.id);
  };

  return (
    <section className="hero">
      <div
        className="hero__bg"
        style={{ backgroundImage: `url(${hero.backdrop_url})` }}
      />
      <div className="hero__shade" />
      <img className="hero__poster" src={hero.backdrop_url} alt="" />
      <div className="hero__content">
        <h1>{hero.name}</h1>
        <p className="hero__meta">
          {hero.rating && <span className="rating">{hero.rating} / 10</span>}
          {hero.year && <span>{hero.year}</span>}
          {hero.genres.slice(0, 3).map((g) => (
            <span key={g}>{g}</span>
          ))}
        </p>
        <p className="hero__overview">{hero.overview}</p>
        <div className="hero__buttons">
          <button className="btn btn--light" onClick={play}>
            ▶ Play
          </button>
          <button className="btn btn--grey" onClick={() => onMoreInfo(hero.id)}>
            ⓘ More Info
          </button>
        </div>
      </div>
    </section>
  );
}
