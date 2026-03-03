import { useRef, useEffect, useState } from "react";
import { motion } from "framer-motion";
import gsap from "gsap";
import type { SearchResult } from "../api/search";
import "./ResultCard.css";

interface Props {
    result: SearchResult;
    rank: number;
    onClick?: (vcId: number) => void;
}

const API_BASE = "http://localhost:8000";

const scoreClass = (score: number) => {
    if (score >= 0.7) return "score-high";
    if (score >= 0.45) return "score-mid";
    return "score-low";
};

function buildThumbnailUrl(src: string): string {
    if (!src) return "";
    // If it's already a full URL, return as-is
    if (src.startsWith("http://") || src.startsWith("https://")) return src;
    // If it's a relative path, prepend API base
    if (src.startsWith("/")) return `${API_BASE}${src}`;
    // Otherwise, assume it's a relative path from API
    return `${API_BASE}/${src}`;
}

function Thumbnail({ src, alt }: { src: string; alt: string }) {
    const [imgLoaded, setImgLoaded] = useState(false);
    const thumbnailUrl = buildThumbnailUrl(src);

    if (!thumbnailUrl) {
        return (
            <motion.div
                className="card-thumb-placeholder"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
            >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M4 4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2H4zm0 2h16v12H4V6zm6.5 2.5a.5.5 0 0 0-.5.5v6a.5.5 0 0 0 .75.43l5-3a.5.5 0 0 0 0-.86l-5-3A.5.5 0 0 0 10.5 8.5z" />
                </svg>
            </motion.div>
        );
    }

    return (
        <motion.div
            className="card-thumb"
            initial={{ opacity: 0 }}
            animate={{ opacity: imgLoaded ? 1 : 0 }}
            transition={{ duration: 0.5 }}
            whileHover={{ scale: 1.05 }}
        >
            <img
                src={thumbnailUrl}
                alt={alt}
                loading="lazy"
                onLoad={() => setImgLoaded(true)}
                onError={(e) => {
                    // Fallback to placeholder on error
                    setImgLoaded(true);
                    (e.currentTarget.style.display) = "none";
                    const parent = e.currentTarget.parentElement as HTMLElement;
                    if (parent) {
                        parent.innerHTML = `<div class="card-thumb-placeholder"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M4 4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2H4zm0 2h16v12H4V6zm6.5 2.5a.5.5 0 0 0-.5.5v6a.5.5 0 0 0 .75.43l5-3a.5.5 0 0 0 0-.86l-5-3A.5.5 0 0 0 10.5 8.5z"/></svg></div>`;
                    }
                }}
            />
        </motion.div>
    );
}

export function ResultCard({ result, rank, onClick }: Props) {
    const pct = Math.round(result.score * 100);
    const cls = scoreClass(result.score);
    const cardRef = useRef<HTMLDivElement>(null);
    const scoreBarRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const card = cardRef.current;
        if (!card) return;

        // Animate score bar on entrance
        const scoreBar = scoreBarRef.current;
        if (scoreBar) {
            gsap.fromTo(
                scoreBar.querySelector(".card-bar-fill"),
                { width: 0 },
                { width: `${pct}%`, duration: 1, delay: 0.3, ease: "power2.out" }
            );
        }

        // Hover effect: lift and shadow
        card.addEventListener("mouseenter", () => {
            gsap.to(card, {
                y: -4,
                boxShadow:
                    "0 20px 40px rgba(0, 0, 0, 0.15), 0 0 1px rgba(0, 0, 0, 0.1)",
                duration: 0.3,
                ease: "power2.out",
            });
        });

        card.addEventListener("mouseleave", () => {
            gsap.to(card, {
                y: 0,
                boxShadow:
                    "0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04)",
                duration: 0.3,
                ease: "power2.out",
            });
        });
    }, [pct]);

    return (
        <motion.article
            ref={cardRef}
            className="result-card"
            onClick={() => onClick && onClick(result.vc_id)}
            style={{ cursor: onClick ? "pointer" : "default" }}
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{
                duration: 0.5,
                delay: rank * 0.08,
                ease: "easeOut",
            }}
            whileHover={{ boxShadow: "0 20px 40px rgba(0, 0, 0, 0.15)" }}
        >
            {/* Thumbnail */}
            <Thumbnail src={result.thumbnail} alt={result.caption || "Video thumbnail"} />

            {/* Body */}
            <div className="card-body">
                {/* Top row: rank + score */}
                <motion.div
                    className="card-header"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.5, delay: rank * 0.08 + 0.1 }}
                >
                    <span className="card-rank">#{rank + 1}</span>
                    <motion.div
                        className={`card-score-badge ${cls}`}
                        initial={{ scale: 0, rotate: -180 }}
                        animate={{ scale: 1, rotate: 0 }}
                        transition={{
                            duration: 0.6,
                            delay: rank * 0.08 + 0.2,
                            type: "spring",
                            stiffness: 100,
                        }}
                    >
                        {pct}%
                    </motion.div>
                </motion.div>

                {/* Caption = video title */}
                <motion.h2
                    className="card-title"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.5, delay: rank * 0.08 + 0.15 }}
                >
                    {result.caption || "(No caption)"}
                </motion.h2>

                {/* Subtopic that was matched */}
                <motion.p
                    className="card-subtopic"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.5, delay: rank * 0.08 + 0.2 }}
                >
                    <span className="subtopic-label">SubTopic</span>
                    {result.subtopic}
                </motion.p>

                {/* File name */}
                {result.file_name && (
                    <motion.p
                        className="card-filename"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.5, delay: rank * 0.08 + 0.25 }}
                    >
                        <span className="filename-icon">📹</span>
                        {result.file_name}
                    </motion.p>
                )}

                {/* Similarity bar */}
                <motion.div
                    ref={scoreBarRef}
                    className="card-bar-row"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.5, delay: rank * 0.08 + 0.3 }}
                >
                    <span className="card-bar-label">Similarity</span>
                    <div
                        className="card-bar-track"
                        role="progressbar"
                        aria-valuenow={pct}
                        aria-valuemin={0}
                        aria-valuemax={100}
                    >
                        <div
                            className={`card-bar-fill ${cls}`}
                            style={{ width: `${pct}%` }}
                        />
                    </div>
                    <span className="card-bar-pct">{result.score.toFixed(3)}</span>
                </motion.div>
            </div>
        </motion.article>
    );
}
