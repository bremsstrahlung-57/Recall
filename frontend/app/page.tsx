export default async function Home() {
    const res = await fetch("http://127.0.0.1:8000/health", {
        cache: "no-store",
    });

    const data = await res.json();

    return <pre>{JSON.stringify(data, null, 2)}</pre>;
}
