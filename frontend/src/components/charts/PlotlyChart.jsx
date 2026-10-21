import createPlotlyComponent from "react-plotly.js/factory";
import Plotly from "plotly.js-dist-min";

const Plot = createPlotlyComponent(Plotly);
export const plotlyLayoutTheme = {
  paper_bgcolor: "transparent",
  plot_bgcolor: "transparent",
  font: { family: "Hanken Grotesk, sans-serif", color: "#0b1c30" },
  colorway: ["#1e1b4b", "#4e45d5", "#38bdf8", "#10b981", "#f59e0b", "#ef4444"],
  margin: { t: 24, r: 16, b: 44, l: 48 },
};

export default function PlotlyChart({ data = [], layout = {}, config = {}, className = "", ...props }) {
  return <div className={`w-full min-w-0 ${className}`}><Plot data={data} layout={{ ...plotlyLayoutTheme, autosize: true, ...layout }} config={{ responsive: true, displaylogo: false, ...config }} useResizeHandler style={{ width: "100%", height: "100%", minHeight: 280 }} {...props} /></div>;
}
