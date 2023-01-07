use rocket;
use rocket::State;
use rocket_dyn_templates::{context, Template};
use std::cmp;
use std::collections::HashMap;
use std::env;
use std::fs;
use std::sync::Arc;
use std::sync::Mutex;

fn read_input_lines(file_name: Option<&str>) -> Vec<String> {
    let file_name = match file_name {
        Some(name) => name,
        None => "input.txt",
    };
    let file: String = fs::read_to_string(file_name).unwrap();
    file.split("\n")
        .map(|x| x.trim())
        .map(|x| String::from(x))
        .filter(|x| x.len() > 0)
        .collect()
}

#[derive(PartialEq, Eq, Hash, Clone)]
struct Position {
    x: i32,
    y: i32,
}

impl Position {
    fn from_string(input_string: &str) -> Position {
        let mut substrings = input_string.split(",").into_iter();
        let x: i32 = substrings.next().unwrap().trim().parse().unwrap();
        let y: i32 = substrings.next().unwrap().trim().parse().unwrap();
        Position { x: x, y: y }
    }
}

const NEW_GRAIN_POSITION: Position = Position { x: 500, y: 0 };

struct Cave {
    min_pos: Position,
    max_pos: Position,
    positions: HashMap<Position, i32>,
    current_grain_pos: Position,
    update_counter: i32,
    number_of_grains: i32,
}

impl Cave {
    fn new(min_pos: Position, max_pos: Position) -> Cave {
        let mut cave = Cave {
            min_pos,
            max_pos,
            positions: HashMap::new(),
            current_grain_pos: NEW_GRAIN_POSITION,
            update_counter: 0,
            number_of_grains: 1,
        };
        cave
    }

    fn min_x(&self) -> i32 {
        self.positions
            .keys()
            .map(|pos| pos.x)
            .min()
            .unwrap_or_default()
    }

    fn min_y(&self) -> i32 {
        0
    }

    fn max_x(&self) -> i32 {
        self.positions
            .keys()
            .map(|pos| pos.x)
            .max()
            .unwrap_or_default()
    }

    fn max_y(&self) -> i32 {
        self.positions
            .keys()
            .map(|pos| pos.y)
            .max()
            .unwrap_or_default()
    }

    fn get(&self, pos: &Position) -> i32 {
        if pos.y > self.max_pos.y + 1 {
            return 1;
        }
        if !(self.positions.contains_key(&pos)) {
            return 0;
        }
        self.positions.get(pos).unwrap().clone()
    }

    fn set(&mut self, pos: &Position, value: i32) {
        self.positions.insert(pos.clone(), value);
    }

    fn draw_rock(&mut self, edges: &Vec<Position>) {
        for edge in edges {
            self.set(&edge, 1);
        }
        for i in 0..edges.len() - 1 {
            let edge1 = edges[i].clone();
            let edge2 = edges[i + 1].clone();
            if edge1.x == edge2.x {
                for y in cmp::min(edge1.y, edge2.y)..cmp::max(edge1.y, edge2.y) {
                    self.set(&Position { x: edge1.x, y: y }, 1)
                }
            }
            if edge1.y == edge2.y {
                for x in cmp::min(edge1.x, edge2.x)..cmp::max(edge1.x, edge2.x) {
                    self.set(&Position { x: x, y: edge1.y }, 1)
                }
            }
        }
    }

    fn paint(&self) -> Vec<Vec<String>> {
        let symbols = HashMap::from([(0, "."), (1, "#"), (2, "°")]);
        let mut output: Vec<Vec<String>> = Vec::new();
        for y in self.min_y()..self.max_y() + 1 {
            let mut line: Vec<String> = Vec::new();
            for x in self.min_x()..self.max_x() + 1 {
                let pos = Position { x: x, y: y };
                let value = self.get(&pos);
                let symbol = symbols[&value];
                line.push(String::from(symbol));
            }
            output.push(line);
        }
        output
    }

    fn move_grain(&mut self) -> bool {
        let below = Position {
            x: self.current_grain_pos.x,
            y: self.current_grain_pos.y + 1,
        };
        let bottom_left = Position {
            x: self.current_grain_pos.x - 1,
            y: self.current_grain_pos.y + 1,
        };
        let bottom_right = Position {
            x: self.current_grain_pos.x + 1,
            y: self.current_grain_pos.y + 1,
        };
        let mut target: Option<Position> = None;
        if self.get(&below) == 0 {
            target = Some(below);
        } else if self.get(&bottom_left) == 0 {
            target = Some(bottom_left);
        } else if self.get(&bottom_right) == 0 {
            target = Some(bottom_right);
        }
        match target {
            None => false,
            Some(pos) => {
                let old_pos = self.current_grain_pos.clone();
                self.set(&old_pos, 0);
                self.set(&pos, 2);
                self.current_grain_pos = pos;
                true
            }
        }
    }

    fn new_grain(&mut self) -> bool {
        if self.get(&NEW_GRAIN_POSITION) != 0 {
            return false;
        }
        self.number_of_grains += 1;
        self.set(&NEW_GRAIN_POSITION, 2);
        self.current_grain_pos = NEW_GRAIN_POSITION;
        true
    }

    fn update(&mut self) -> bool {
        let moved = self.move_grain();
        if !moved {
            let new_grain_created = self.new_grain();
            if !new_grain_created {
                return false;
            }
        }
        self.update_counter += 1;
        true
    }
}

fn parse_input(input_lines: &Vec<String>) -> Vec<Vec<Position>> {
    let mut output = Vec::new();
    for line in input_lines.iter() {
        let tuple_strings = line.split("->");
        output.push(
            tuple_strings
                .collect::<Vec<&str>>()
                .iter()
                .map(|tuple_string| Position::from_string(tuple_string.trim()))
                .collect::<Vec<Position>>(),
        )
    }
    output
}

fn get_dimensions(parsed_input: &Vec<Vec<Position>>) -> (Position, Position) {
    let mut min_x = 10000;
    let min_y = 0;
    let mut max_x = -100000;
    let mut max_y = -100000;
    for path in parsed_input {
        for position in path {
            min_x = cmp::min(min_x, position.x);
            max_x = cmp::max(max_x, position.x);
            max_y = cmp::max(max_y, position.y);
        }
    }
    (
        Position { x: min_x, y: min_y },
        Position { x: max_x, y: max_y },
    )
}

fn iterate_for_result(mut cave: Cave) {
    loop {
        let updated = cave.update();
        if cave.update_counter % 1000 == 0 {
            println!(
                "grain {} at iteration {}",
                cave.number_of_grains, cave.update_counter
            );
        }
        if cave.current_grain_pos.y > cave.max_pos.y {
            println!(
                "The first grain to fall through is number {} at iteration {}.",
                cave.number_of_grains, cave.update_counter
            );
            break;
        }
    }
    loop {
        let updated = cave.update();
        if !updated {
            println!(
                "grain {} at iteration {}, Update failed",
                cave.number_of_grains, cave.update_counter
            );
            break;
        }
        if cave.update_counter % 100000 == 0 {
            println!(
                "grain {} at iteration {}",
                cave.number_of_grains, cave.update_counter
            );
        }
    }
}

#[rocket::get("/")]
fn index(cave: &State<Arc<Mutex<Cave>>>) -> Template {
    let mut cave = cave.lock().unwrap();
    Template::render(
        "index",
        context! {
            number_of_grains: cave.number_of_grains,
            update_counter: cave.update_counter,
            cave: cave.paint()
        },
    )
}

#[rocket::get("/cave")]
fn render_cave(cave: &State<Arc<Mutex<Cave>>>) -> Template {
    let mut cave = cave.lock().unwrap();
    Template::render(
        "index",
        context! {
            number_of_grains: cave.number_of_grains,
            update_counter: cave.update_counter,
            cave: cave.paint()
        },
    )
}
#[rocket::get("/update-cave")]
fn update_cave(mut cave: &State<Arc<Mutex<Cave>>>) -> Template {
    let mut cave = cave.lock().unwrap();
    let last_grain = cave.number_of_grains;
    while last_grain / 10 == cave.number_of_grains / 10 {
        let updated = cave.update();
        if !updated {
            break;
        }
    }
    Template::render(
        "index",
        context! {
            number_of_grains: cave.number_of_grains,
            update_counter: cave.update_counter,
            cave: cave.paint()
        },
    )
}

#[rocket::main]
async fn main() {
    let input_lines = read_input_lines(Some("input.txt"));
    let parsed_input = parse_input(&input_lines);
    let (min_pos, max_pos) = get_dimensions(&parsed_input);
    let mut cave = Cave::new(min_pos, max_pos);
    for edges in parsed_input {
        cave.draw_rock(&edges);
    }
    let args: Vec<String> = env::args().collect();
    if args.contains(&String::from("web")) {
        rocket::build()
            .manage(Arc::from(Mutex::from(cave)))
            .mount("/", rocket::routes![index, render_cave, update_cave])
            .mount("/static", rocket::fs::FileServer::from("static"))
            .attach(Template::fairing())
            .launch()
            .await;
    } else {
        iterate_for_result(cave);
    }
}

#[cfg(test)]
#[test]
fn test_create_position() {
    let position = Position::from_string("59, 10");
    assert_eq!(position.x, 59);
    assert_eq!(position.y, 10);
}

#[test]
fn test_parse_input() {
    let input_lines = read_input_lines(Some("test_input.txt"));
    let parsed_input = parse_input(&input_lines);
    assert_eq!(parsed_input[0].len(), 3);
    assert_eq!(parsed_input[1][2].x, 502);
}

#[test]
fn test_get_dimensions() {
    let input_lines = read_input_lines(Some("test_input.txt"));
    let parsed_input = parse_input(&input_lines);
    let (min_pos, max_pos) = get_dimensions(&parsed_input);
    assert_eq!(min_pos.x, 494);
    assert_eq!(min_pos.y, 0);
    assert_eq!(max_pos.x, 503);
    assert_eq!(max_pos.y, 9);
}

#[test]
fn test_draw_matrix() {
    let input_lines = read_input_lines(Some("test_input.txt"));
    let parsed_input = parse_input(&input_lines);
    let (min_pos, max_pos) = get_dimensions(&parsed_input);
    let mut cave = Cave::new(min_pos, max_pos);
    for edges in parsed_input {
        cave.draw_rock(&edges);
    }
    let pic = cave.paint();
    assert_eq!(pic.len(), 10);
    assert_eq!(pic[4][4], String::from("#"));
    assert_eq!(pic[4][5], String::from("."));
}
