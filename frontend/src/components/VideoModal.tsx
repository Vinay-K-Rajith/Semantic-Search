import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import { X } from "lucide-react";
import "./VideoModal.css";

interface VideoModalProps {
  vcId: number;
  onClose: () => void;
  videoEndTime?: number | null;
}

declare global {
  interface Window {
    vdo: any;
  }
}

const API_URL = import.meta.env.VITE_CIPHER_API_URL;
const API_TOKEN = import.meta.env.VITE_CIPHER_API_TOKEN;
const API_KEY = import.meta.env.VITE_CIPHER_API_KEY;
const CIPHER_SCHOOL_CODE = import.meta.env.VITE_CIPHER_SCHOOL_CODE;
const CIPHER_THEME = import.meta.env.VITE_CIPHER_THEME;

export function VideoModal({ vcId, onClose, videoEndTime }: VideoModalProps) {
  const [playbackInfo, setPlaybackInfo] = useState<string | null>(null);
  const [otp, setOtp] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [vdoReady, setVdoReady] = useState(false);

  const embedBoxRef = useRef<HTMLDivElement>(null);
  const videoIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Load vdo.js script
  useEffect(() => {
    const loadVdoScript = () => {
      // Check if already loaded
      if (window.vdo) {
        console.log("vdo already loaded");
        setVdoReady(true);
        return;
      }

      console.log("Loading vdo.js script...");
      /* global vdo */
      (function (v: any, i: Document, d: string, e: string, o: string) {
        v[o] = v[o] || {};
        v[o].add =
          v[o].add ||
          function V(a: any) {
            (v[o].d = v[o].d || []).push(a);
          };
        if (!v[o].l) {
          v[o].l = 1 * new Date().getTime();
          let a = i.createElement(d) as HTMLScriptElement,
            m = i.getElementsByTagName(d)[0];
          a.async = true;
          a.src = e;
          a.onload = () => {
            console.log("vdo.js script loaded");
            setVdoReady(true);
          };
          if (m && m.parentNode) {
            m.parentNode.insertBefore(a, m);
          }
        }
      })(
        window,
        document,
        "script",
        "https://player.vdocipher.com/playerAssets/1.6.10/vdo.js",
        "vdo"
      );
    };

    loadVdoScript();
  }, []);

  // Fetch video details
  useEffect(() => {
    if (!vdoReady) return;

    const fetchVideoDetails = async () => {
      setIsLoading(true);
      setError(null);
      try {
        console.log("Fetching video details for vcId:", vcId);

        const response = await axios.post(
          API_URL + "api/StudentPortal/LMSVideoCipher",
          {
            flag: "GetCiphervideoStream",
            value: vcId.toString(),
            Device: false,
            Key: API_KEY,
          },
          {
            headers: {
              Authorization: API_TOKEN,
              Schoolcode: "Entab",
            },
          }
        );

        console.log("API Response:", response.data);

        if (response.data && response.data.classDetails) {
          try {
            const classDetails = JSON.parse(response.data.classDetails);
            console.log("Parsed classDetails:", classDetails);

            if (classDetails.otp && classDetails.playbackInfo) {
              setOtp(classDetails.otp);
              setPlaybackInfo(classDetails.playbackInfo);
              setIsLoading(false);
            } else {
              setError(
                "Invalid playback data: missing otp or playbackInfo"
              );
              setIsLoading(false);
            }
          } catch (parseErr: any) {
            console.error("Error parsing classDetails:", parseErr);
            setError("Failed to parse video details");
            setIsLoading(false);
          }
        } else {
          setError("Failed to get playback information from API");
          setIsLoading(false);
        }
      } catch (err: any) {
        console.error("Error fetching video:", err);
        setError(
          err.response?.data?.message ||
            err.message ||
            "Failed to fetch video details"
        );
        setIsLoading(false);
      }
    };

    fetchVideoDetails();
  }, [vcId, vdoReady]);

  // Initialize video player
  useEffect(() => {
    if (
      !playbackInfo ||
      !otp ||
      !vdoReady ||
      !embedBoxRef.current ||
      !window.vdo
    ) {
      return;
    }

    console.log("Initializing vdo player with otp and playbackInfo");

    // Clear previous content
    if (embedBoxRef.current) {
      embedBoxRef.current.innerHTML = "";
    }

    try {
      window.vdo.add({
        otp: otp,
        playbackInfo: playbackInfo,
        theme: CIPHER_THEME,
        container: embedBoxRef.current,
      });

      // Seek video if videoEndTime is provided
      if (videoEndTime !== null && videoEndTime !== undefined) {
        console.log("Setting up video seek to:", videoEndTime);

        function seekVideo() {
          if (window.vdo) {
            try {
              const videos = window.vdo.getObjects();
              if (videos && videos.length > 0) {
                const video = videos[videos.length - 1];
                if (
                  video &&
                  video.statusText &&
                  video.statusText !== "loading"
                ) {
                  if (videoEndTime != null && videoEndTime !== "") {
                    let seekPosition = parseInt(videoEndTime.toString());
                    if (seekPosition >= 10) {
                      seekPosition = seekPosition - 10;
                    }
                    console.log(
                      "Seeking video to position:",
                      seekPosition
                    );
                    video.seek(seekPosition.toString());
                  }
                  if (videoIntervalRef.current) {
                    clearInterval(videoIntervalRef.current);
                    videoIntervalRef.current = null;
                  }
                }
              }
            } catch (seekErr) {
              console.error("Error seeking video:", seekErr);
            }
          }
        }

        const videoInterval = setInterval(seekVideo, 500);
        videoIntervalRef.current = videoInterval;

        // Clear interval after 10 seconds to avoid infinite loop
        const timeoutId = setTimeout(() => {
          if (videoIntervalRef.current) {
            clearInterval(videoIntervalRef.current);
            videoIntervalRef.current = null;
          }
        }, 10000);

        return () => {
          clearTimeout(timeoutId);
          if (videoIntervalRef.current) {
            clearInterval(videoIntervalRef.current);
          }
        };
      }
    } catch (initErr) {
      console.error("Error initializing vdo player:", initErr);
      setError("Failed to initialize video player");
    }
  }, [playbackInfo, otp, vdoReady, videoEndTime]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (videoIntervalRef.current) {
        clearInterval(videoIntervalRef.current);
      }
    };
  }, []);

  return (
    <div className="video-modal-overlay" onClick={onClose}>
      <div
        className="video-modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <button className="video-modal-close" onClick={onClose}>
          <X size={24} />
        </button>
        <div
          style={{
            position: "relative",
            width: "100%",
            height: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          {(isLoading || !vdoReady) && (
            <div className="video-loading">
              Loading video player...
            </div>
          )}
          {error && (
            <div className="video-error">
              <p>{error}</p>
              <p style={{ fontSize: "0.9rem", marginTop: "10px" }}>
                vcId: {vcId}
              </p>
            </div>
          )}
          <div
            ref={embedBoxRef}
            id="embedBox"
            style={{
              width: "100%",
              height: "100%",
              borderRadius: "10px",
              display:
                isLoading || error || !vdoReady ? "none" : "block",
              border: 0,
            }}
          ></div>
        </div>
      </div>
    </div>
  );
}
