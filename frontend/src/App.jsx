import { useEffect, useState } from "react";
import { fetchHomepage } from "./services/api";
import Navbar from "./components/Navbar";
import HeroBanner from "./components/HeroBanner";
import Row from "./components/Row";
import TitleModal from "./components/TitleModal";
import Loading from "./components/Loading";
import ErrorState from "./components/ErrorState";

export default function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(true);
  const [selectedId, setSelectedId] = useState(null);

  const load = () => {
    setLoading(true);
    setError(false);
    fetchHomepage()
      .then(setData)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  return (
    <>
      <Navbar />
      {loading && <Loading />}
      {error && <ErrorState onRetry={load} />}
      {data && (
        <main>
          <HeroBanner hero={data.hero} onMoreInfo={setSelectedId} />
          <div className="rows">
            {data.rows.length === 0 && (
              <p className="empty">
                Nothing here yet. Run <code>python manage.py sync_catalog</code>{" "}
                in the backend folder, then refresh.
              </p>
            )}
            {data.rows.map((row) => (
              <Row key={row.slug} row={row} onSelect={setSelectedId} />
            ))}
          </div>
        </main>
      )}
      {selectedId && (
        <TitleModal id={selectedId} onClose={() => setSelectedId(null)} />
      )}
    </>
  );
}
