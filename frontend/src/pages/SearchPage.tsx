import { useState, useCallback, useEffect, useRef } from "react";
import { AlertCircle, Play, Pause } from "lucide-react";
import { motion } from "framer-motion";
import gsap from "gsap";
import { SearchBar } from "../components/SearchBar";
import { ResultCard } from "../components/ResultCard";
import { VideoModal } from "../components/VideoModal";
import { semanticSearch, healthCheck } from "../api/search";
import type { SearchResponse } from "../api/search";
import "./SearchPage.css";

type Status = "idle" | "loading" | "done" | "error";

export function SearchPage() {
    const [status, setStatus] = useState<Status>("idle");
    const [response, setResponse] = useState<SearchResponse | null>(null);
    const [errorMsg, setErrorMsg] = useState("");
    const [backendOk, setBackendOk] = useState<boolean | null>(null);
    const [isPlaying, setIsPlaying] = useState(true);
    const [selectedVcId, setSelectedVcId] = useState<number | null>(null);
    const [videoEndTime, setVideoEndTime] = useState<number | null>(null);
    const videoRef = useRef<HTMLVideoElement>(null);

    // Ping backend health once on mount
    useEffect(() => {
        healthCheck().then(setBackendOk);
    }, []);

    const handleVideoClick = useCallback((vcId: number) => {
        setSelectedVcId(vcId);
        setVideoEndTime(null); // Reset seek position for new video
    }, []);

    const handleSearch = useCallback(async (query: string, topK: number) => {
        setStatus("loading");
        setResponse(null);
        setErrorMsg("");
        
        // Minimum 3 seconds loading display
        const startTime = Date.now();
        
        try {
            const data = await semanticSearch(query, topK);
            const elapsed = Date.now() - startTime;
            const delayRemaining = Math.max(0, 3000 - elapsed);
            
            // Wait for remaining time to reach 3 seconds
            if (delayRemaining > 0) {
                await new Promise(resolve => setTimeout(resolve, delayRemaining));
            }
            
            setResponse(data);
            setStatus("done");
        } catch (err: unknown) {
            const msg =
                err instanceof Error ? err.message : "Unknown error occurred";
            setErrorMsg(msg);
            setStatus("error");
        }
    }, []);

    const toggleVideo = () => {
        if (videoRef.current) {
            if (isPlaying) {
                videoRef.current.pause();
            } else {
                videoRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    return (
        <main className="search-page">
            {/* Hero Section with Video */}
            <motion.section
                className="hero-section"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8 }}
            >
                {/* Left: Title & Description */}
                <motion.div
                    className="hero-content"
                    initial={{ opacity: 0, x: -40 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.8, delay: 0.1 }}
                >
                    <motion.h1
                        className="hero-title"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.7, delay: 0.2 }}
                    >
                        Find Meaning,
                        <br />
                        Not Just Keywords
                    </motion.h1>

                    <motion.p
                        className="hero-description"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.7, delay: 0.3 }}
                    >
                        Search your video library with AI-powered semantic understanding. 
                        Get relevant results based on meaning, not just matching words.
                    </motion.p>
                </motion.div>

                {/* Right: Video Player */}
                <motion.div
                    className="hero-video-container"
                    initial={{ opacity: 0, x: 40 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                >
                    <div className="video-wrapper">
                        <video
                            ref={videoRef}
                            className="video-player"
                            loop
                            autoPlay
                            muted
                            playsInline
                        >
                            <source src="/education.mp4" type="video/mp4" />
                            Your browser does not support the video tag.
                        </video>
                        
                        <motion.button
                            className="video-play-btn"
                            onClick={toggleVideo}
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                        >
                            {isPlaying ? (
                                <Pause size={24} fill="white" />
                            ) : (
                                <Play size={24} fill="white" />
                            )}
                        </motion.button>

                        <div className="video-gradient" />
                    </div>
                </motion.div>
            </motion.section>

            {/* Search Bar */}
            <motion.section
                className="search-hero-section"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.3 }}
            >
                {backendOk === false && (
                    <motion.div
                        className="banner banner-warn"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        <AlertCircle size={16} />
                        Backend not reachable. Start uvicorn on port 8000.
                    </motion.div>
                )}
                <SearchBar onSearch={handleSearch} isLoading={status === "loading"} />
            </motion.section>

            {/* Results Section */}
            <section className="results-section">
                {status === "loading" && (
                    <motion.div
                        className="state-loading"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.4 }}
                    >
                        <motion.p
                            className="loading-tagline"
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.1 }}
                        >
                            Find meaning, not just keywords
                        </motion.p>
                        <div className="loading-video-container">
                            <video
                                className="loading-video"
                                autoPlay
                                loop
                                muted
                                playsInline
                            >
                                <source src="/ani.mp4" type="video/mp4" />
                            </video>
                        </div>
                    </motion.div>
                )}

                {status === "error" && (
                    <motion.div
                        className="banner banner-error"
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        <AlertCircle size={16} />
                        {errorMsg}
                    </motion.div>
                )}

                {status === "done" && response && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.5 }}
                    >
                        <div className="results-meta">
                            <motion.div
                                className="results-header"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ duration: 0.5 }}
                            >
                                <span className="result-count">{response.total}</span>
                                <span className="result-label">results for</span>
                                <em className="query-text">"{response.query}"</em>
                                <span className="result-time">{response.time_ms}ms</span>
                            </motion.div>
                        </div>

                        <motion.div
                            className="results-grid"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ staggerChildren: 0.08, delayChildren: 0.1 }}
                        >
                            {response.results.map((r, i) => (
                                <ResultCard 
                                    key={r.vc_id} 
                                    result={r} 
                                    rank={i}
                                    onClick={handleVideoClick}
                                />
                            ))}
                        </motion.div>
                    </motion.div>
                )}

                {status === "idle" && (
                    <motion.div
                        className="state-idle"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                    >
                        <motion.div
                            className="idle-illustration"
                            animate={{ y: [0, -8, 0] }}
                            transition={{ duration: 3, repeat: Infinity }}
                        >
                            ✨
                        </motion.div>
                        <p className="idle-text">
                            Start searching to discover videos by meaning and context
                        </p>
                    </motion.div>
                )}
            </section>

            {/* Video Modal */}
            {selectedVcId !== null && (
                <VideoModal
                    vcId={selectedVcId}
                    onClose={() => setSelectedVcId(null)}
                    videoEndTime={videoEndTime}
                />
            )}
        </main>
    );
}
