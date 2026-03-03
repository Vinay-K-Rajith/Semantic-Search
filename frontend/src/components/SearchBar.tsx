import { useState, useRef, useCallback } from "react";
import { Search, X, Loader2 } from "lucide-react";
import { motion } from "framer-motion";
import "./SearchBar.css";

interface Props {
    onSearch: (query: string, topK: number) => void;
    isLoading: boolean;
}

const TOP_K_OPTIONS = [3, 5, 8, 10];

export function SearchBar({ onSearch, isLoading }: Props) {
    const [query, setQuery] = useState("");
    const [topK, setTopK] = useState(5);
    const inputRef = useRef<HTMLInputElement>(null);
    const boxRef = useRef<HTMLDivElement>(null);

    const handleSubmit = useCallback(
        (q = query) => {
            if (q.trim()) onSearch(q.trim(), topK);
        },
        [query, topK, onSearch]
    );

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter") handleSubmit();
    };

    const clearQuery = () => {
        setQuery("");
        inputRef.current?.focus();
    };

    return (
        <motion.div
            className="searchbar-root"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut", delay: 0.1 }}
        >
            <motion.div
                ref={boxRef}
                className="searchbar-box"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                whileHover={{ 
                    boxShadow: "0 12px 32px rgba(0, 188, 212, 0.12)",
                    y: -2
                }}
            >
                <div className="searchbar-icon">
                    <Search size={20} />
                </div>
                <input
                    ref={inputRef}
                    id="search-input"
                    type="text"
                    className="searchbar-input"
                    placeholder="Search by topic, concept, or question…"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                    aria-label="Semantic search query"
                    autoFocus
                />
                {query && (
                    <motion.button
                        className="searchbar-clear"
                        onClick={clearQuery}
                        aria-label="Clear query"
                        initial={{ opacity: 0, scale: 0.5 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.5 }}
                        transition={{ duration: 0.2 }}
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                    >
                        <X size={16} />
                    </motion.button>
                )}

                <div className="searchbar-divider" />

                {/* Top-K selector */}
                <label className="sr-only" htmlFor="topk-select">
                    Results count
                </label>
                <motion.select
                    id="topk-select"
                    className="searchbar-topk"
                    value={topK}
                    onChange={(e) => setTopK(Number(e.target.value))}
                    aria-label="Number of results"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                >
                    {TOP_K_OPTIONS.map((k) => (
                        <option key={k} value={k}>
                            Top {k}
                        </option>
                    ))}
                </motion.select>

                <motion.button
                    id="search-btn"
                    className="searchbar-btn"
                    onClick={() => handleSubmit()}
                    disabled={isLoading || !query.trim()}
                    aria-label="Search"
                    whileHover={{ scale: !isLoading && query.trim() ? 1.02 : 1 }}
                    whileTap={{ scale: !isLoading && query.trim() ? 0.98 : 1 }}
                >
                    {isLoading ? (
                        <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        >
                            <Loader2 size={18} />
                        </motion.div>
                    ) : (
                        <span>Search</span>
                    )}
                </motion.button>
            </motion.div>
        </motion.div>
    );
}
