#!/usr/bin/env node

const { execSync, spawnSync } = require("child_process");
const path = require("path");
const os = require("os");
const fs = require("fs");
const https = require("https");
const readline = require("readline");

// Colors
const RED = "\x1b[31m";
const GREEN = "\x1b[32m";
const BLUE = "\x1b[34m";
const YELLOW = "\x1b[33m";
const NC = "\x1b[0m"; // No Color

const args = process.argv.slice(2);
const command = args[0] || "help";

const homeDir = os.homedir();
const installDir = path.join(homeDir, ".lodestone");
const configDir = path.join(homeDir, ".config", "lodestone");
const composeFile = path.join(installDir, "docker-compose.yml");

function runCmd(cmd, args = []) {
    const result = spawnSync(cmd, args, { stdio: "inherit" });

    if (result.error) {
        console.error(`Failed to run: ${cmd} ${args.join(" ")}`);
        console.error(result.error.message);
        process.exit(1);
    }

    if (result.status !== 0) {
        process.exit(result.status || 1);
    }
}

function downloadFile(url, dest) {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(dest);

        https
            .get(url, (response) => {
                if (response.statusCode !== 200) {
                    file.close(() => fs.unlink(dest, () => {}));
                    return reject(
                        new Error(`Download failed: ${response.statusCode}`),
                    );
                }

                response.pipe(file);
                file.on("finish", () => file.close(resolve));
            })
            .on("error", (err) => {
                file.close(() => fs.unlink(dest, () => {}));
                reject(err);
            });
    });
}

function showHelp() {
    console.log(`${BLUE}Lodestone CLI${NC}`);
    console.log(`Usage: lodestone [COMMAND]

Commands:
  start   Start the Lodestone containers
  stop    Stop the Lodestone containers
  update  Update compose files, pull latest images, and restart
  delete  Stop containers and remove Docker images (keeps data/volumes)
  prune   Stop containers, remove images, volumes, and installation data (keeps config)
  logs    Tail the container logs
`);
}

function promptConfirm(question) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });
    return new Promise((resolve) => {
        rl.question(question, (answer) => {
            rl.close();
            resolve(answer.toLowerCase() === "y");
        });
    });
}

async function setup() {
    if (!fs.existsSync(installDir))
        fs.mkdirSync(installDir, { recursive: true });
    if (!fs.existsSync(configDir)) fs.mkdirSync(configDir, { recursive: true });

    const composeUrl =
        "https://raw.githubusercontent.com/bremsstrahlung-57/lodestone/master/docker-compose.prod.yml";
    console.log(`${YELLOW}Downloading latest docker-compose.yml...${NC}`);
    await downloadFile(composeUrl, composeFile);
}

async function main() {
    if (command === "help") {
        showHelp();
        process.exit(0);
    }

    if (!fs.existsSync(installDir) && command !== "start") {
        console.error(
            `${RED}Lodestone is not installed in ${installDir}.${NC}`,
        );
        console.error("Please run the 'start' command first to install.");
        process.exit(1);
    }

    try {
        execSync("docker --version", { stdio: "ignore" });
    } catch {
        console.error(
            `${RED}Error: Docker is not installed or not running.${NC}`,
        );
        process.exit(1);
    }

    switch (command) {
        case "start":
            await setup();
            console.log(`${YELLOW}Starting Lodestone...${NC}`);
            runCmd("docker", ["compose", "-f", composeFile, "up", "-d"]);
            console.log(`${GREEN}Started! Web UI: http://localhost:8090${NC}`);
            break;
        case "stop":
            console.log(`${YELLOW}Stopping Lodestone...${NC}`);
            runCmd("docker", ["compose", "-f", composeFile, "down"]);
            console.log(`${GREEN}Lodestone stopped.${NC}`);
            break;
        case "update":
            await setup();
            console.log(`${YELLOW}Updating images...${NC}`);
            runCmd("docker", ["compose", "-f", composeFile, "pull"]);
            console.log(
                `${YELLOW}Restarting containers with new configurations and images...${NC}`,
            );
            runCmd("docker", [
                "compose",
                "-f",
                composeFile,
                "up",
                "-d",
                "--remove-orphans",
            ]);
            console.log(`${GREEN}Update complete!${NC}`);
            break;
        case "delete":
            console.log(
                `${YELLOW}Removing Lodestone containers and local images...${NC}`,
            );
            runCmd("docker", [
                "compose",
                "-f",
                composeFile,
                "down",
                "--rmi",
                "local",
            ]);
            console.log(
                `${GREEN}Images and containers deleted. (Volumes and configs were kept)${NC}`,
            );
            break;
        case "prune":
            console.log(
                `${RED}WARNING: This will completely destroy all Lodestone data and images. (Config will be kept)${NC}`,
            );
            const confirmed = await promptConfirm(
                "Are you sure you want to continue? [y/N] ",
            );
            if (confirmed) {
                console.log(
                    `${YELLOW}Stopping containers and removing volumes/images...${NC}`,
                );
                runCmd("docker", [
                    "compose",
                    "-f",
                    composeFile,
                    "down",
                    "-v",
                    "--rmi",
                    "all",
                ]);
                console.log(`${YELLOW}Removing installation directory...${NC}`);
                fs.rmSync(installDir, { recursive: true, force: true });
                console.log(
                    `${GREEN}Lodestone has been completely pruned from your system.${NC}`,
                );
            } else {
                console.log("Prune cancelled.");
            }
            break;
        case "logs":
            runCmd("docker", ["compose", "-f", composeFile, "logs", "-f"]);
            break;
        default:
            showHelp();
            process.exit(1);
    }
}

main();
