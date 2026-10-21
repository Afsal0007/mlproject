import { Link } from "react-router-dom";
import { Button, PageHeader } from "../components/ui/index.jsx";

export default function NotFoundPage() {
  return <div className="flex flex-col gap-6"><PageHeader eyebrow="404 / Not Found" title="This page could not be found" subtitle="The address may have changed or you may not have access to this route." /><Link to="/"><Button>Return to dashboard</Button></Link></div>;
}
