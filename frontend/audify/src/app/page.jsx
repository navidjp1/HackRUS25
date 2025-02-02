"use client";

import Image from "next/image";
import { useState } from "react";

export default function Home() {
    const [selectedLanguage, setSelectedLanguage] = useState("Translate?");
    const [selectedVoice, setSelectedVoice] = useState("Female Voice");
    const [showLanguages, setShowLanguages] = useState(false);
    const [showVoices, setShowVoices] = useState(false);
    const [url, setUrl] = useState("");
    const [error, setError] = useState("");
    const [pageState, setPageState] = useState("input"); // "input", "loading", or "download"
    const [audioFiles, setAudioFiles] = useState([]);
    const [isLoadingNext, setIsLoadingNext] = useState(false);
    const [currentPart, setCurrentPart] = useState(1);
    const [isComplete, setIsComplete] = useState(false);

    const languages = [
        "Translate?",
        "English",
        "Spanish",
        "French",
        "Hindi",
        "Portuguese",
    ];
    const voices = ["Female Voice", "Male Voice"];

    const handleCreateAudiobook = async () => {
        if (!url.trim()) {
            setError("Please enter a URL");
            return;
        }

        setError("");
        setPageState("loading");
        setAudioFiles([]);
        setCurrentPart(1);
        setIsComplete(false);

        try {
            await fetchPart(1);
            setPageState("download");
        } catch (err) {
            setError("Failed to create audiobook. Please try again.");
            console.error("Error:", err);
            setPageState("input");
        }
    };

    const fetchPart = async (partNumber) => {
        setIsLoadingNext(true);
        try {
            const response = await fetch("http://localhost:4000/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    url: url,
                    language: selectedLanguage,
                    voice: selectedVoice,
                    part: partNumber,
                }),
            });

            if (!response.ok) {
                if (response.status === 404) {
                    // No more parts available
                    setIsLoadingNext(false);
                    setIsComplete(true);
                    return;
                }
                throw new Error(`Failed to load part ${partNumber}`);
            }

            const blob = await response.blob();
            const downloadURL = window.URL.createObjectURL(blob);
            setAudioFiles((prev) => [...prev, { url: downloadURL, part: partNumber }]);
            setCurrentPart(partNumber);
            setIsLoadingNext(false);

            // Start fetching next part
            fetchPart(partNumber + 1);
        } catch (err) {
            if (err.message.includes("404")) {
                setIsComplete(true);
                setIsLoadingNext(false);
            } else {
                console.error(`Error loading part ${partNumber}:`, err);
                setError(`Failed to load part ${partNumber}. Please try again.`);
            }
        }
    };

    // Dropdown component to reduce code duplication
    const Dropdown = ({ show, options, selected, onSelect, onToggle }) => (
        <div className="relative">
            <button
                className="px-4 py-2 bg-black text-white border border-gray-300 rounded-lg hover:bg-gray-800 font-[Inter] min-w-[120px] flex justify-between items-center"
                onClick={onToggle}
            >
                {selected} <span className="ml-2">▼</span>
            </button>
            {show && (
                <ul className="absolute left-0 mt-2 bg-black text-white border border-gray-300 rounded-lg p-2 w-40 z-10">
                    {options.map((option) => (
                        <li
                            key={option}
                            className="py-1 px-2 hover:bg-gray-800 cursor-pointer flex justify-between items-center"
                            onClick={() => onSelect(option)}
                        >
                            {option}
                            {selected === option && " ✅"}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );

    const InputView = () => (
        <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
            <h1 className="text-white text-8xl text-center font-bold font-[Inter] w-full">
                AUDIFY
            </h1>
            <div className="relative w-[40rem]">
                <input
                    type="text"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Enter url..."
                    className="w-full h-12 p-4 border border-gray-300 rounded-lg bg-black text-white font-[Inter] focus:outline-none placeholder:text-gray-400"
                />
                {error && <p className="text-red-500 mt-2 text-sm">{error}</p>}
            </div>

            <div className="flex justify-between w-[40rem] gap-4">
                <Dropdown
                    show={showLanguages}
                    options={languages}
                    selected={selectedLanguage}
                    onSelect={(lang) => {
                        setSelectedLanguage(lang);
                        setShowLanguages(false);
                    }}
                    onToggle={() => {
                        setShowLanguages(!showLanguages);
                        setShowVoices(false);
                    }}
                />

                <Dropdown
                    show={showVoices}
                    options={voices}
                    selected={selectedVoice}
                    onSelect={(voice) => {
                        setSelectedVoice(voice);
                        setShowVoices(false);
                    }}
                    onToggle={() => {
                        setShowVoices(!showVoices);
                        setShowLanguages(false);
                    }}
                />

                <button
                    onClick={handleCreateAudiobook}
                    className="px-6 py-2 bg-black text-white border border-gray-300 rounded-lg hover:bg-gray-800 font-[Inter] transition-colors duration-200"
                >
                    Create Audiobook
                </button>
            </div>
        </main>
    );

    const LoadingView = () => (
        <main className="flex flex-col gap-8 row-start-2 items-center">
            <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-white"></div>
            <h2 className="text-white text-2xl font-[Inter] text-center">
                Generating your audiobook...
                <br />
                <span className="text-gray-400 text-lg">
                    Please wait a couple of minutes
                </span>
            </h2>
        </main>
    );

    const DownloadView = () => (
        <main className="flex flex-col gap-8 row-start-2 items-center">
            <h2 className="text-white text-4xl font-[Inter] mb-8">
                {isComplete
                    ? "Your Audiobook is Ready!"
                    : `Part ${currentPart} is Ready!`}
            </h2>
            <div className="bg-gray-900 rounded-lg p-6 w-[40rem]">
                <div className="flex flex-col gap-4">
                    {audioFiles.map((file, index) => (
                        <div key={index} className="flex flex-col gap-2">
                            <div className="flex justify-between items-center bg-black p-4 rounded-lg border border-gray-700">
                                <span className="text-white font-[Inter]">
                                    Part {index + 1}
                                </span>
                                <a
                                    href={file.url}
                                    download={`audiobook_part${index + 1}.mp3`}
                                    className="px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors duration-200"
                                >
                                    Download
                                </a>
                            </div>
                            {index + 1 === currentPart && isLoadingNext && (
                                <div className="flex items-center justify-center gap-2 text-gray-400 py-2">
                                    <div className="w-4 h-4 border-t-2 border-b-2 border-gray-400 rounded-full animate-spin"></div>
                                    <span>Loading Part {currentPart + 1}...</span>
                                </div>
                            )}
                        </div>
                    ))}
                </div>

                {isComplete && (
                    <button
                        onClick={() => {
                            setPageState("input");
                            setUrl("");
                            setAudioFiles([]);
                            setCurrentPart(1);
                            setIsComplete(false);
                            setIsLoadingNext(false);
                        }}
                        className="mt-6 w-full px-4 py-2 bg-black text-white border border-gray-300 rounded-lg hover:bg-gray-800 font-[Inter] transition-colors duration-200"
                    >
                        Convert Another Book
                    </button>
                )}
            </div>
        </main>
    );

    return (
        <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
            {pageState === "input" && <InputView />}
            {pageState === "loading" && <LoadingView />}
            {pageState === "download" && <DownloadView />}
        </div>
    );
}
