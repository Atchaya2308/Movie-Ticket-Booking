import smtplib
import mysql.connector

def connect():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345',
        database='ticketbooking'
    )

def add_booking(cursor, booker_name, theater_name, movie_title, number_of_tickets, seat_numbers, total_amount):
    query = """
    INSERT INTO bookings (booker_name, theater_name, movie_title, number_of_tickets, seat_numbers, total_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (booker_name, theater_name, movie_title, number_of_tickets, seat_numbers, total_amount))

def get_bookings(cursor):
    query = "SELECT * FROM bookings"
    cursor.execute(query)
    return cursor.fetchall()

def read_movies(file_path):
    movies = []
    with open(file_path, 'r') as file:
        for line in file:
            title, price = line.strip().split(',')
            movies.append((title, float(price)))
    return movies

def display_movies(movies):
    for theater, movie_list in movies.items():
        print(f"Theater: {theater}")
        for title, price in movie_list:
            print(f"  Movie: {title}, Price: {price:.2f}")

def send_email(booker_name, booker_email, theater_name, movie_title, number_of_tickets, seat_numbers, total_amount):
     
    body = (
        f"Dear {booker_name},\n\n"
        f"Thank you for booking with us!\n"
        f"Theater: {theater_name}\n"
        f"Movie: {movie_title}\n"
        f"Tickets: {number_of_tickets}\n"
        f"Seats: {seat_numbers}\n"
        f"Total Amount: {total_amount:.2f}\n\n"
        f"Enjoy the show!\n"
       f"Thankyou for booking\n"
    )
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login("atchayaananth2005@gmail.com","kegb abbl fpid bvgx")
    s.sendmail("atchayaananth2005@gmail.com",booker_email,body)
    s.quit()
    print("Mail sent Successfully")

def main():
    db = connect()
    cursor = db.cursor()

    # Read movie details from text files
    theaters = {
        "Vasu Theater": "theater1.txt",
        "Kasi Theater": "theater2.txt",
        "MSM Theater": "theater3.txt"
    }
    movie_data = {theater: read_movies(file) for theater, file in theaters.items()}

    # Display movies
    display_movies(movie_data)

    # Booking process
    booker_name = input("Enter your name: ")
    booker_email = input("Enter your email: ")
    theater_name = input("Enter theater name: ")
    movie_title = input("Enter movie title: ")
    number_of_tickets = int(input("Enter number of tickets: "))
    seat_numbers = input("Enter seat numbers (comma-separated): ")

    # Calculate total amount
    movie_price = None
    for theater, movies in movie_data.items():
        if theater == theater_name:
            for title, price in movies:
                if title == movie_title:
                    movie_price = price
                    break

    if movie_price is None:
        print("Movie not found!")
        return

    total_amount = number_of_tickets * movie_price
    print(f"Total amount: {total_amount:.2f}")

    # Add booking to database
    add_booking(cursor, booker_name, theater_name, movie_title, number_of_tickets, seat_numbers, total_amount)
    db.commit()

    # Append booking details to a file
    with open('bookings.txt', 'a') as file:
        file.write(f"Name: {booker_name}, Theater: {theater_name}, Movie: {movie_title}, "
                   f"Tickets: {number_of_tickets}, Seats: {seat_numbers}, Total Amount: {total_amount:.2f}\n")

    # Send confirmation email
    send_email(booker_name, booker_email, theater_name, movie_title, number_of_tickets, seat_numbers, total_amount)

    # Display all bookings
    bookings = get_bookings(cursor)
    for booking in bookings:
        print(booking)

    cursor.close()
    db.close()

if __name__ == "__main__":
     main()
