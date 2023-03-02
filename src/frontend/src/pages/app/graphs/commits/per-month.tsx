import axios from "axios";
import { useQuery } from "react-query";
import { Radar } from "react-chartjs-2";
import { OneToNArray } from "../../utils";


type CommitsPerMonthResponse = Record<number, number>

const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const ZERO = 0;


export default function CommitsPerMonth() {
    const query = useQuery<CommitsPerMonthResponse>(
        ["commits-per-month"],
        () => axios.get("/commits-per-month").then(response => response.data),
    );
    if (query.isLoading) {
        return <>Loading...</>;
    }
    if (query.isError) {
        return <>Error...</>;
    }

    return <Radar data={{
        labels: MONTHS,
        datasets: [{
            label: "Avg Commits per Month",
            data: OneToNArray(MONTHS.length).map(i => query.data![i] ?? ZERO),
            borderColor: "#F05133",
        }],
    }} options={{
        // maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: "Avg Commits per Month",
            },
            legend: {
                display: false,
            },
        },
        interaction: {
            intersect: false,
        },
        elements: {
            line: {
                tension: 0.25,
            },
        },
        scales: {
            r: {
                ticks: {
                    display: false,
                },
                grid: {
                    color: "white",
                },
            },
        },
    }} width="100%" height="100%" className="w-full" />;
}