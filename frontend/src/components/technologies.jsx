import * as React from "react";
import ActionAreaCard from "./card";
import { Link } from "react-router-dom";

export default function Technologies() {
  return (
    <div className="py-8">
      <h2 className="text-center text-4xl font-bold mb-8">
        Our Technologies
      </h2>
      <div className="flex justify-center flex-wrap gap-8 p-10">
        <Link to="/general">
        <ActionAreaCard 
          image="https://tse3.mm.bing.net/th?id=OIP.VF70pDXwrj1N5MD672fICQHaEK&pid=Api&P=0&h=180"
          title="Kidney Diagnosis"
          description="Online checkup of your kidney with the power of AI"
        />
        </Link>
        <Link to="treatment">
        <ActionAreaCard 
          image="https://tse1.mm.bing.net/th?id=OIP.b-ZIB8_xCuxBqmI_Lagh4wHaDm&pid=Api&P=0&h=180"
          title="Treatment Plan"
          description="If the previous test states your kidney is not healthy, identify if you have any kidney diseases"
        />
        </Link >

        <Link to="plan">
        <ActionAreaCard 
          image="https://tse2.mm.bing.net/th?id=OIP.Vb_ISef7DKY4lje7SGoYgQHaEL&pid=Api&P=0&h=180"
          title="Feedback"
          description="Identify your problems and allow us to guide you in your treatment process"
        />
        </Link>
      </div>
    </div>
  );
}
