from PIL import Image
import random

# Function to convert text to binary
def text_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

# Function to convert binary to text
def binary_to_text(binary_text):
    text = ''
    for i in range(0, len(binary_text), 8):
        text += chr(int(binary_text[i:i+8], 2))
    return text

# Function to hide text in image using ILSB
def hide_text_in_image_ilsb(text, image_path):
    binary_text = text_to_binary(text)
    image = Image.open(image_path)
    width, height = image.size
    max_bits_to_hide = width * height * 3  # 3 channels (RGB) per pixel

    if len(binary_text) > max_bits_to_hide:
        raise ValueError("Text too long to hide in the image")

    binary_index = 0
    pixels = image.load()
    for row in range(height):
        for col in range(width):
            pixel = list(pixels[col, row])  # Convert to list to modify pixel values
            if binary_index < len(binary_text):
                for i in range(3):  # Iterate over RGB channels
                    if binary_index < len(binary_text):
                        pixel[i] = (pixel[i] & ~1) | int(binary_text[binary_index])
                        binary_index += 1
            pixels[col, row] = tuple(pixel)  # Convert back to tuple and assign to pixel

            if binary_index >= len(binary_text):
                break

        if binary_index >= len(binary_text):
            break

    new_image_path = 'hidden_image2.png'
    image.save(new_image_path)
    return new_image_path

# Function to extract text from image using ILSB
def extract_text_from_image_ilsb(image_path):
    image = Image.open(image_path)
    width, height = image.size
    binary_text = ''

    pixels = image.load()
    for row in range(height):
        for col in range(width):
            pixel = pixels[col, row]
            for channel_value in pixel[:3]:  # Iterate over RGB channels
                binary_text += str(channel_value & 1)

    return binary_to_text(binary_text)

# Genetic Algorithm parameters
population_size = 50
mutation_rate = 0.01
num_generations = 100

# Function to perform genetic algorithm
def genetic_algorithm(target_text):
    text_length = len(target_text)
    population = generate_population(text_length)

    for generation in range(num_generations):
        # Evaluate fitness
        fitness_scores = [(chromosome, fitness(chromosome, target_text)) for chromosome in population]
        fitness_scores.sort(key=lambda x: x[1])  # Sort by fitness

        # Check if we've reached the target
        if fitness_scores[0][1] == 0:
            return fitness_scores[0][0]

        # Selection: Keep the top performers
        top_performers = [chromosome for chromosome, _ in fitness_scores[:10]]

        # Crossover: Create new individuals through crossover of top performers
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(top_performers, 2)
            crossover_point = random.randint(0, text_length - 1)
            child = parent1[:crossover_point] + parent2[crossover_point:]
            new_population.append(child)

        # Mutation: Introduce random mutations
        for i in range(len(new_population)):
            if random.random() < mutation_rate:
                mutate_index = random.randint(0, text_length - 1)
                new_population[i] = new_population[i][:mutate_index] + ('1' if new_population[i][mutate_index] == '0' else '0') + new_population[i][mutate_index + 1:]

        population = new_population

    return None

# Function to generate initial population
def generate_population(text_length):
    population = []
    for _ in range(population_size):
        chromosome = ''.join(random.choice(['0', '1']) for _ in range(text_length))
        population.append(chromosome)
    return population

# Function to evaluate fitness of a chromosome
def fitness(chromosome, target_text):
    differences = sum(1 for c1, c2 in zip(chromosome, target_text) if c1 != c2)
    return differences

# Example usage
if __name__ == "__main__":
    # Encode text in image using ILSB
    text_to_hide = "helllo this  is working!!!"
    image_path = r"emojipng.png" # Provide the path to your PNG image
    hidden_image_path = hide_text_in_image_ilsb(text_to_hide, image_path)
    
    # Display the original and encoded images with their names
    print("Original Image:", image_path)
    Image.open(image_path).show()
    
    print("Encoded Image:", hidden_image_path)
    Image.open(hidden_image_path).show()
