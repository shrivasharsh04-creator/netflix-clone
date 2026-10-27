export default function ErrorState({ onRetry }) {
  return (
    <div className="error-state">
      <h2>Something went wrong</h2>
      <p>
        We couldn't load the shows. Make sure the backend is running on port
        8000, then try again.
      </p>
      <button className="btn btn--light" onClick={onRetry}>
        Try again
      </button>
    </div>
  );
}
