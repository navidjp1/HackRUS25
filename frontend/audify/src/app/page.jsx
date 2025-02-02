"use client";

import Image from "next/image";
import { useState } from "react";

export default function Home() {
    const [selectedLanguage, setSelectedLanguage] = useState("English");
    const [showLanguages, setShowLanguages] = useState(false);
    const languages = ["English", "Spanish", "French", "Hindi", "Portuguese"];

    return (
        <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
            <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
                <h1 className="text-white text-8xl text-center font-bold font-[Inter] w-full">
                    AUDIFY
                </h1>
                <div className="relative w-[30rem]">
                    <input
                        type="text"
                        placeholder="Enter url..."
                        className="w-full h-8 p-2 border border-gray-300 rounded-lg bg-black text-white font-[Inter] focus:outline-none placeholder:text-white"
                    />
                </div>

                {/* Buttons Row */}
                <div className="flex justify-between w-[30rem]">
                    {/* Languages Dropdown Button */}
                    <div className="relative">
                        <button
                            className="px-4 py-2 bg-black text-white border border-gray-300 rounded-lg hover:bg-gray-800 font-[Inter]"
                            onClick={() => setShowLanguages(!showLanguages)}
                        >
                            {selectedLanguage}
                        </button>
                        {showLanguages && (
                            <ul className="absolute left-0 mt-2 bg-black text-white border border-gray-300 rounded-lg p-2 w-40">
                                {languages.map((language) => (
                                    <li
                                        key={language}
                                        className="py-1 px-2 hover:bg-gray-800 cursor-pointer flex justify-between"
                                        onClick={() => {
                                            setSelectedLanguage(language);
                                            setShowLanguages(false);
                                        }}
                                    >
                                        {language}
                                        {selectedLanguage === language && " ✅"}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>

                    {/* Create Audiobook Button */}
                    <button className="px-4 py-2 bg-black text-white border border-gray-300 rounded-lg hover:bg-gray-800 font-[Inter]">
                        Create Audiobook
                    </button>
                </div>
            </main>
        </div>
    );
}
