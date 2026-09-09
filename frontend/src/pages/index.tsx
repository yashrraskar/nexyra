import { useEffect } from "react";
import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/dashboard");
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 text-xs font-mono text-slate-500">
      Redirecting to MahaSync Citizen Dashboard...
    </div>
  );
}
