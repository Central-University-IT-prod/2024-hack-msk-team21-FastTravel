import "./welcome.css";
import Link from "next/link";

export default function Home() {
  return (
      <div className="bg_1">
        <div className="bg_2">

        </div >
        <a id="title">FastTravel</a>
        <Link href="/login" >
          <button className="btn" id="login_button">Присоединиться</button>
        </Link>
      </div>
  );
}