import { PageHeader } from "../components/ui/index.jsx";

export default function SectionPage({ eyebrow, title, subtitle }) {
  return <div className="flex flex-col gap-space-lg"><PageHeader eyebrow={eyebrow} title={title} subtitle={subtitle} /></div>;
}
