/**
 * When each file's content last changed, from `git log --name-status -M` output
 * (newest commit first). A pure rename (R100) is not a change: the date follows
 * the file back to its old path, so moving the pages keeps their dates.
 */
export function lastEdits(log: string): Map<string, string> {
  const dates = new Map<string, string>();
  const currentName = new Map<string, string>(); // an older path -> the path it has now
  const current = (path: string) => currentName.get(path) ?? path;
  const touch = (path: string, date: string) => {
    if (!dates.has(path)) dates.set(path, date);
  };
  let date = "";
  for (const line of log.split("\n")) {
    if (line.startsWith("@")) {
      date = line.slice(1);
      continue;
    }
    const [status, ...paths] = line.split("\t");
    if (!status || !paths.length) continue;
    if (status.startsWith("R") || status.startsWith("C")) {
      const [from, to] = paths;
      const now = current(to);
      if (status.startsWith("R")) currentName.set(from, now);
      if (status !== "R100") touch(now, date);
    } else if (status !== "D") {
      touch(current(paths[0]), date);
    }
  }
  return dates;
}
