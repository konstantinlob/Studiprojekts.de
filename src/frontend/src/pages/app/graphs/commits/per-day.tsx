import axios from "axios";
import { useQuery } from "react-query";
import { Bar } from "react-chartjs-2";
import { OneToNArray } from "../../utils";


type CommitsPerDayResponse = Record<number, number>

const DAYS_PER_MONTH = 31;
const ZERO = 0;


export default function CommitsPerDay() {
    const query = useQuery<CommitsPerDayResponse>(
        ["commits-per-day"],
        () => axios.get("/commits-per-day").then(response => response.data),
    );
    if (query.isLoading) {
        return <>Loading...</>;
    }
    if (query.isError) {
        return <>Error...</>;
    }

    const days = OneToNArray(DAYS_PER_MONTH);

    return <Bar data={{
        labels: days,
        datasets: [{
            label: "Avg Commits per Day",
            data: days.map(i => query.data![i] ?? ZERO),
            backgroundColor: "#F05133",
        }],
    }} options={{
        // maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: "Avg Commits per Day",
            },
            legend: {
                display: false,
            },
        },
        interaction: {
            intersect: false,
        },
    }} width="100%" height="100%" className="w-full max-h-screen" />;
}