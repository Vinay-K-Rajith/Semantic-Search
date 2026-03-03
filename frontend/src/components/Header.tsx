import { Brain } from "lucide-react";
import { motion } from "framer-motion";
import gsap from "gsap";
import { useEffect, useRef } from "react";
import "./Header.css";

export function Header() {
    const logoIconRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const icon = logoIconRef.current;
        if (!icon) return;

        // Gentle floating animation on the brain icon
        gsap.to(icon, {
            y: -4,
            duration: 2,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut",
        });
    }, []);

    return (
        <motion.header
            className="header"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
        >
            <div className="header-inner">
                <motion.div
                    className="header-logo"
                    whileHover={{ scale: 1.02 }}
                    transition={{ duration: 0.3 }}
                >
                    <motion.div
                        ref={logoIconRef}
                        className="logo-icon"
                        whileHover={{ rotate: 360 }}
                        transition={{ duration: 0.6 }}
                    >
                        <Brain size={22} strokeWidth={2} />
                    </motion.div>
                    <div className="logo-text">
                        <motion.span
                            className="logo-name"
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.6, delay: 0.1 }}
                        >
                            SemanticSearch
                        </motion.span>
                        <motion.span
                            className="logo-badge"
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.6, delay: 0.15 }}
                        >
                            FAISS · MiniLM
                        </motion.span>
                    </div>
                </motion.div>
            </div>
        </motion.header>
    );
}
