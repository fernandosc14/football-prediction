"use client";

import { motion } from "framer-motion";

export default function ConfidenceBar({ confidence }: { confidence: number }) {
  return (
    <div className="w-full mt-4">
      <div className="flex justify-between items-center mb-1">
        <span className="text-xs font-semibold text-slate-400">Confidence</span>
        <span className="text-sm font-bold text-white">{confidence}%</span>
      </div>
      <div className="w-full bg-slate-800 rounded-full h-2.5">
        <motion.div
          className="bg-gradient-to-r from-cyan-400 to-blue-600 h-2.5 rounded-full"
          initial={{ width: 0 }}
          whileInView={{ width: `${confidence}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          viewport={{ once: true }}
        />
      </div>
    </div>
  );
}
