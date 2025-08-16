
Skip to content
Navigation Menu
boikot-xyz
boikot

Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights

    Settings

Owner avatar
boikot
Public

boikot-xyz/boikot
t
Name	Last commit message
	Last commit date
OscarSaharoy
OscarSaharoy
add to MCP info in readme
4489ae8
 · 
Aug 10, 2025
ads
	
more design
	
Feb 18, 2024
backend
	
ignore tyo
	
Apr 20, 2024
mcp
	
add rewrite for /mcp route
	
Aug 10, 2025
scripts
	
update render.jsto es6
	
Aug 4, 2025
site
	
add png favicon
	
Aug 10, 2025
.gitignore
	
add boikot.json to mcp server files
	
Aug 10, 2025
.vercelignore
	
add vercelignore
	
Aug 10, 2025
LICENSE.txt
	
Create LICENSE
	
Dec 10, 2023
README.md
	
add to MCP info in readme
	
Aug 10, 2025
boikot.json
	
amazon companies
	
Aug 8, 2025
todo.txt
	
update todo
	
Aug 6, 2025
Repository files navigation

README

    GPL-3.0 license

boikot 🙅‍♀️

boikot is a community-led initiative to make data on company ethics transparent and accessible.

We are building a community-curated, transparent, freely accessible collection of corporate ethics records. By documenting ethical and unethical business practices, we aim to inform consumer choice, raise the cost of harmful business decisions, and incentivise companies to act responsibly in the public interest.

All of our services and data are offered free to the public under the terms of the GPL v3 licence. You can download our full companies dataset from the file called boikot.json above.

The main product being worked on is the boikot.xyz website which provides access to our data and tools to add new records to it. This is a react project in the site directory. There also some tools for collecting and summarising information in the scripts and backend directories.
MCP

We also have an MCP server that exposes a tool to lookup company ethics information. This is available from the URL https://mcp.boikot.xyz/mcp with no authentication needed. It proviedes one tool called lookup_company_information which takes one parameter company_name and returns information about the company's ethics.
the dataset

the boikot.json file is a database of the ethical and unethical practices of different companies. Each item in the "companies" object represents a company ethics record. Each of these items has a "names" areay containing names that can be used for the company, of which the first entry is the most commonly used name. They also have a "comment" string which is a comment on the ethics of the company, with sources denoted by numbers in square brackets eg. [1][2]. The URLs for these sources are in the "sources" object which is a mapping from the source numbers to URLs. Each company also has tags in the "tags" array, which are strings that describe the company. Finally each company has a "logoUrl" and "siteUrl" which are URLs for the company's logo image and website. There is an "updatedAt" timestamp on each item to track when it was last updated.
links

Corporate Research site: https://www.corp-research.org/home-page

Impact of boycotts on McDonalds: https://m.youtube.com/watch?v=K9Uf3eUWKE8
bookmarks

These are some bookmarks that make it a bit faster to collect the company data. They add JSON data into your clipboard that you can then paste into the "Merge JSON" thing on the company edit page

Get company website and logo when on its wikipedia page:

javascript:( () => {     const logoImg =         document.querySelector(".infobox-image.logo img") ??         document.querySelector(".infobox-image img");      const logoURL = logoImg?.src         .replace("thumb/", "")         .replace(/^\/\/upload/, "https://upload")         .replace(/\/[^/]+.(png|jpg)$/, "");      const infoBoxLabels = [...document.querySelectorAll(         "table.infobox tr"     )];      const siteLabel = infoBoxLabels.filter(          el => el.innerHTML.includes("Website")             || el.innerHTML.includes("URL")     )[0];      const siteURL = siteLabel?.querySelector("a").href;        navigator.clipboard.writeText(`{ "logoUrl": "${logoURL}", "siteUrl": "${siteURL}" }`); } )()

Copy the url of the current page as a new source:

javascript:( async () => {     const clipboardString = await navigator.clipboard.readText();     let clpiboard;     try {         clipboard = JSON.parse(clipboardString);     } catch (e) {         clipboard = {};     }     const nextKey = Math.max(0, ...Object.keys(clipboard?.sources || {})) + 1;      navigator.clipboard.writeText(JSON.stringify({ ...clipboard, sources: { ...( clipboard?.sources || {}), [nextKey.toString()]: window.location.href } })); } )()

About

boikot
boikot.xyz
Resources
Readme
License
GPL-3.0 license
Activity
Custom properties
Stars
1 star
Watchers
1 watching
Forks
0 forks
Report repository
Releases
No releases published
Create a new release
Packages
No packages published
Publish your first package
Deployments 16

Production August 10, 2025 12:31

    Preview August 10, 2025 12:30

+ 14 deployments
Languages

HTML 78.0%
JavaScript 21.9%

    Other 0.1% 

Suggested workflows
Based on your tech stack

    SLSA Generic generator logo
    SLSA Generic generator

Generate SLSA3 provenance for your existing release workflows
Node.js logo
Node.js
Build and test a Node.js project with npm.
Publish Node.js Package to GitHub Packages logo
Publish Node.js Package to GitHub Packages

    Publishes a Node.js package to GitHub Packages.

More workflows
Footer
© 2025 GitHub, Inc.
Footer navigation

    Terms
    Privacy
    Security
    Status
    Docs
    Contact


