import { useState } from "react";

const App = () => {
  const [formData, setFormData] = useState({ url: "", scans: [] });
  const [selectAll, setSelectAll] = useState(false);
  const [data, setData] = useState();

  const allScans = ["dns", "seched", "tls", "whois", "ports", "techdet"];

  const handleCheckboxChange = (e) => {
    const { value, checked } = e.target;

    const updatedScans = checked
      ? [...formData.scans, value]
      : formData.scans.filter((scan) => scan !== value);

    setFormData((prev) => ({
      ...prev,
      scans: updatedScans,
    }));

    setSelectAll(updatedScans.length === allScans.length);
  };

  const handleSelectAllChange = (e) => {
    const checked = e.target.checked;

    setSelectAll(checked);

    setFormData((prev) => ({
      ...prev,
      scans: checked ? allScans : [],
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    fetchScan();

    console.log("STATE DATA", formData);
    console.log("STATE STRING DATA", JSON.stringify(formData));
  };

  const fetchScan = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8001/api/scan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          domain: formData.url,
          checks: formData.scans,
        }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const result = await response.json();
      console.log(result);
      setData(result);
    } catch (error) {
      console.error("Fetch error:", error);
    }
  };

  return (
    <div className="h-screen p-6">
      <div className="flex gap-[2ch] items-center flex-col h-full p-8 bg-gray-300">
        <h1>URL SEARCH TOOL</h1>
        <form className="" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Input URL"
            value={formData.url}
            onChange={(e) =>
              setFormData((prev) => ({
                ...prev,
                url: e.target.value,
              }))
            }
          />

          <div className="flex flex-col">
            <label>
              <input
                type="checkbox"
                value="dns"
                checked={formData.scans.includes("dns")}
                onChange={handleCheckboxChange}
              />
              DNS lookup
            </label>

            <label>
              <input
                type="checkbox"
                value="seched"
                checked={formData.scans.includes("seched")}
                onChange={handleCheckboxChange}
              />
              Security Headers
            </label>

            <label>
              <input
                type="checkbox"
                value="tls"
                checked={formData.scans.includes("tls")}
                onChange={handleCheckboxChange}
              />
              TLS Certificate (Under developement)
            </label>

            <label>
              <input
                type="checkbox"
                value="whois"
                checked={formData.scans.includes("whois")}
                onChange={handleCheckboxChange}
              />
              WHOIS
            </label>

            <label>
              <input
                type="checkbox"
                value="ports"
                checked={formData.scans.includes("ports")}
                onChange={handleCheckboxChange}
              />
              Port Scan
            </label>

            <label>
              <input
                type="checkbox"
                value="techdet"
                checked={formData.scans.includes("techdet")}
                onChange={handleCheckboxChange}
              />
              Technology Detection
            </label>

            <br />

            <label>
              <input
                type="checkbox"
                value="all"
                checked={selectAll}
                onChange={handleSelectAllChange}
              />
              Select All
            </label>

            <br />
          </div>

          <input
            className="bg-white cursor-pointer px-4 py-2"
            value="Search"
            type="submit"
          />
        </form>
      </div>
    </div>
  );
};

export default App;
